# Technical Report: Optimal Training Parameters for SDXL LoRA Training

This report outlines the recommended base model and training parameters for Low-Rank Adaptation (LoRA) training on Stable Diffusion XL (SDXL), tailored for efficient fine-tuning of high-quality image generation models. The information is compiled from community resources, tutorials, and configuration examples, with a focus on practical settings for use with tools like Kohya SS GUI.

## Base Model

The optimal base model for SDXL LoRA training is `stabilityai/stable-diffusion-xl-base-1.0`, available on Hugging Face ([Hugging Face SDXL Base Model](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)). This model, developed by Stability AI, is designed for high-resolution (1024x1024) text-to-image generation, offering enhanced photorealism, better face generation, and improved text handling compared to earlier Stable Diffusion models. It serves as a robust foundation for LoRA fine-tuning, allowing adaptation to specific styles, characters, or objects while maintaining the model’s core capabilities.

## Training Parameters

LoRA training for SDXL involves configuring several parameters to balance model performance, training speed, and hardware constraints. Below is a detailed breakdown of key parameters, based on a synthesis of community recommendations and a sample configuration from a GitHub Gist ([Kohya SS Config](https://gist.github.com/pixelass/446c3cafde6bd81d4f2de01f8ce9b8ee)), Medium articles ([Comprehensive Guide](https://medium.com/%40guillaume.bieler/a-comprehensive-guide-to-training-a-stable-diffusion-xl-lora-optimal-settings-dataset-building-844113a6d5b3)), and Reddit discussions ([Reddit Guide](https://www.reddit.com/r/StableDiffusion/comments/1gvp073/a_personal_experience_guide_to_training_sdxl/)).

### Key Parameters

| **Parameter**                | **Value/Setting**                     | **Notes**                                                                 |
|------------------------------|---------------------------------------|---------------------------------------------------------------------------|
| **Optimizer**                | Adafactor or AdamW                    | Adafactor with learning rate 0.0004; AdamW with 3e-05. Prodigy with Cosine also used for automatic LR adjustment. |
| **Learning Rate**            | 0.0004 (Adafactor), 3e-05 (AdamW)     | Adjust based on optimizer and dataset. Higher rates may reduce flexibility. |
| **Network Dimension (Rank)** | 32 or 64                              | Higher rank (e.g., 64) for complex datasets; 16 for low VRAM (8GB).        |
| **Network Alpha**            | 1 or 32                               | Often set equal to rank; lower values (e.g., 1) scale effective learning rate. |
| **Batch Size**               | 1–4                                   | 1 for 8GB VRAM, 2–3 for 12GB, 5+ for 24GB+. Higher sizes speed up training. |
| **Epochs**                   | 8–30                                  | Adjust based on dataset size; 1500–3000 steps often targeted.              |
| **Max Resolution**           | 1024,1024                             | Native SDXL resolution; lower (e.g., 768x768) for low VRAM with quality trade-off. |
| **Mixed Precision**          | bf16 or fp16                          | bf16 for 12GB+ VRAM; fp16 for 8GB VRAM. Enhances memory efficiency.       |
| **Gradient Checkpointing**   | True                                  | Reduces VRAM usage by recomputing gradients.                              |
| **Xformers**                 | True                                  | Enables memory-efficient attention mechanisms.                            |
| **Min SNR Gamma**            | 5                                     | Improves convergence speed; recommended for latent diffusion models.       |
| **Save Every N Epochs**      | 1–10                                  | Save checkpoints frequently to monitor progress and avoid overfitting.     |

### Example Configuration

Below is an example configuration derived from a Kohya SS JSON file for SDXL LoRA training:

| **Parameter**                | **Value**                     |
|------------------------------|-------------------------------|
| LoRA_type                    | Standard                     |
| learning_rate                | 0.0004                       |
| text_encoder_lr              | 0.0004                       |
| unet_lr                      | 0.0004                       |
| network_dim                  | 64                           |
| network_alpha                | 1                            |
| train_batch_size             | 1                            |
| epoch                        | 8                            |
| max_resolution               | 1024,1024                    |
| mixed_precision              | bf16                         |
| gradient_checkpointing       | true                         |
| xformers                     | true                         |
| optimizer                    | Adafactor                    |
| optimizer_args               | scale_parameter=False, relative_step=False, warmup_init=False |
| lr_scheduler                 | constant                     |
| save_model_as                | safetensors                  |
| sdxl                         | true                         |

This configuration is a starting point, but parameters like learning rate, batch size, and epochs may need adjustment based on specific datasets and hardware.

## Dataset Preparation

- **Image Quality and Quantity**: Use 50–100 high-quality images at 1024x1024 resolution. For low VRAM setups, 16–30 images can suffice if carefully curated to include diverse angles (e.g., close-ups, full-body shots).
- **Captioning**: Accurate captions are critical. Tools like JoyCaption ([GitHub JoyCaption](https://github.com/D3voz/joy-caption-alpha-two-gui-mod)) can automate captioning, but manual editing ensures clarity and relevance. Use unique tokens (e.g., “df4gf man”) to avoid bleeding from real-world names.
- **Folder Structure**: For Kohya SS, organize images in a folder with a repeat rate (e.g., “3_” prefix for 3 repeats). Example: `/mnt/private/train/My_Images`.

## Hardware Requirements

- **Ideal Setup**: A GPU with 24GB VRAM supports batch sizes of 2–5, enabling faster training (e.g., ~1 hour for 2000 steps on a Tesla V100).
- **Low VRAM (8GB)**: Possible with batch size 1, network rank 16, and alpha 1, but training may take 60+ hours for 2000 steps. Use 768x768 or 512x512 resolution to reduce memory demands, accepting a quality trade-off.
- **Cloud Options**: Services like RunPod or Google Colab can provide high-VRAM GPUs for efficient training.

## Additional Considerations

- **Optimizer Choice**: Adafactor and AdamW are common, but Prodigy with Cosine scheduler offers automatic learning rate adjustment, potentially simplifying tuning ([OneTrainer Optimizers](https://github.com/Nerogar/OneTrainer/wiki/Optimizers)).
- **Overfitting Risks**: Monitor for signs like distorted outputs or inability to generalize beyond training data. Adjust epochs or steps (100–400 per image) to balance likeness and flexibility.
- **Sampling and Checkpoints**: Sample every 10 epochs or 200 steps to track progress. Save checkpoints frequently to evaluate model quality and revert if needed.
- **Community Variations**: Some users report success with higher network ranks (e.g., 128) or alpha values (e.g., 8) for style-focused LoRAs, but these increase memory demands ([Reddit SDXL Settings](https://www.reddit.com/r/sdforall/comments/15dr0b2/what_settings_are_you_using_for_sdxl_kohya/)).

## Recommendations for Experimentation

Given the variability in community recommendations, start with the example configuration above and adjust based on:
- **Dataset Size**: Smaller datasets (20–30 images) may require fewer epochs (8–15) to avoid overfitting.
- **Hardware**: Lower batch size and rank for 8GB VRAM; increase for 24GB+ VRAM.
- **Task**: For style LoRAs, higher ranks (64–128) may capture more detail; for character LoRAs, lower ranks (16–32) may suffice.

Experimentation is key, as optimal settings depend on the specific use case. Monitor training logs for loss values and generated samples to fine-tune parameters.

## Citations

- [Kohya SS GitHub](https://github.com/bmaltais/kohya_ss)
- [SDXL Base Model on Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- [Medium Article on SDXL LoRA Training](https://medium.com/%40guillaume.bieler/a-comprehensive-guide-to-training-a-stable-diffusion-xl-lora-optimal-settings-dataset-building-844113a6d5b3)
- [Reddit Post on SDXL LoRA Training](https://www.reddit.com/r/StableDiffusion/comments/1gvp073/a_personal_experience_guide_to_training_sdxl/)
- [GitHub Gist with Config](https://gist.github.com/pixelass/446c3cafde6bd81d4f2de01f8ce9b8ee)
- [Civitai SDXL LoRA Training Guide](https://civitai.com/articles/10872/training-sdxl-lora-in-kohyass-with-8gb-12gb-or-higher-vram)
- [Aituts LoRA Training Settings](https://aituts.com/lora-training-settings/)
- [ThinkDiffusion SDXL LoRA Tutorial](https://learn.thinkdiffusion.com/creating-sdxl-lora-models-on-kohya/)
