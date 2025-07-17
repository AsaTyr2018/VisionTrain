# Technical Report: Optimal LoRA Training Parameters for SDXL-Based PonyXL Model

## Introduction
This report provides a comprehensive guide to training a Low-Rank Adaptation (LoRA) model on the Stable Diffusion XL (SDXL) architecture, specifically targeting results similar to the PonyXL model, a fine-tuned SDXL variant known for its vibrant anime, cartoon, furry, and pony-themed imagery. The focus is on identifying the best base model and optimal training parameters, tailored for a technical audience (AI systems) requiring precise, actionable information. The recommendations are derived from community resources, including guides from Civitai, Medium, and Hugging Face, ensuring a robust foundation for achieving high-quality LoRA models.

## Best Base Model
The **Pony Diffusion V6 XL** is the recommended base model for training a LoRA that aligns closely with PonyXL’s capabilities. This model, available at [Civitai](https://civitai.com/models/257749/pony-diffusion-v6-xl), is a fine-tuned version of SDXL, optimized for generating high-quality images in anime, cartoon, and character-driven styles. Its training dataset includes approximately 2.6 million images with a balanced 1:1 ratio of anime/cartoon/furry/pony content and safe/questionable/explicit ratings, making it ideal for capturing the dynamic and versatile output of PonyXL.

### Alternative Base Model
If a closer alignment to the original SDXL is preferred, the **stabilityai/stable-diffusion-xl-base-1.0** ([Hugging Face](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)) can be used. However, this may require a dataset and tagging strategy that mimics PonyXL’s training data to achieve similar results, which could be more complex due to the lack of PonyXL’s specific fine-tuning.

## Training Parameters
The following parameters are optimized for training a LoRA on Pony Diffusion V6 XL, based on the “SDXL Pony Fast Training Guide” ([Civitai](https://civitai.com/models/351583/sdxl-pony-fast-training-guide)) and its associated preset ([JSON](https://files.catbox.moe/t5clrs.json)). These settings are tailored for a dataset of 20–40 images, suitable for character or style adaptation.

| **Parameter**                     | **Value**                     | **Notes**                                                                 |
|-----------------------------------|-------------------------------|---------------------------------------------------------------------------|
| Optimizer                        | Prodigy                      | Dynamically adjusts learning rate for efficient training.                  |
| Learning Rate                    | 1.0                          | Default for Prodigy; automatically adjusted during training.               |
| LR Scheduler                     | Cosine                       | Ensures smooth learning rate decay over epochs.                           |
| Network Dimension (Rank)         | 16                           | Low rank for small datasets to prevent overfitting; suitable for 20–40 images. |
| Network Alpha                    | 2                            | Complements low rank for compact adaptation.                              |
| Batch Size                       | 3                            | Balances training speed and GPU memory usage.                             |
| Epochs                           | 50                           | Sufficient for small datasets; adjust based on convergence.               |
| Mixed Precision                  | bf16                         | Reduces memory demands while maintaining precision.                       |
| Gradient Checkpointing           | Enabled                      | Conserves VRAM, essential for lower-spec GPUs (e.g., 10–12GB).            |
| Additional Optimizer Arguments   | weight_decay=0.01, d_coef=1, use_bias_correction=True, safeguard_warmup=False, betas=0.9,0.99 | Specific to Prodigy for stable optimization.                              |
| Resolution Settings              | max_resolution=1024,1024, min_bucket_reso=512, max_bucket_reso=2048, bucket_reso_steps=256 | Supports bucketing for variable image sizes.                              |
| Save Frequency                   | Every 10 epochs              | Suggested to save every 5 epochs for closer monitoring.                   |

### Parameter Variations
Community practices show variations in parameters depending on dataset size and style complexity:
- **Network Dimension and Alpha**: Some LoRAs use dim=32 and alpha=32 for larger datasets or more complex styles, as seen in models like “Gold Filigree XL and Pony” ([Civitai](https://civitai.com/models/571004/gold-filigree-xl-and-pony)). Lower values (dim=16, alpha=2) are preferred for smaller datasets to avoid overfitting.
- **Optimizer**: While Prodigy is common, some use Adafactor with a learning rate of 0.0005, as in “Andy Kubert PDXL” ([Civitai](https://civitai.com/models/388048)).
- **Steps/Epochs**: Total steps range from 2560 to 8160, with epochs between 6–12 for larger datasets, indicating flexibility based on training goals.

## Dataset Recommendations
The quality and composition of the training dataset significantly impact LoRA performance. The following guidelines are based on PonyXL’s training data and community best practices:
- **Number of Images**: 20–40 high-quality images, preferably from the same illustrator or series for consistency (e.g., zunko dataset, [Catbox](https://files.catbox.moe/lnelg0.zip)).
- **Resolution**: At least 1024x1024 pixels, aligning with SDXL’s native resolution. Bucketing (min_bucket_reso=512, max_bucket_reso=2048) allows flexibility for varied sizes.
- **Tagging**: Use the moat-tagger-v2 model with a threshold of 0.35 for accurate autotagging. Include quality tags like “score_9, source_anime” and a unique trigger word (e.g., “znkAA”) to associate with the character or concept.
- **Captioning**: Approximately 50% of PonyXL’s training images had high-quality captions, suggesting detailed captions for at least half the dataset. Avoid overly complex captions; keep them short and relevant.
- **Data Filtering**: Remove undesirable tags (e.g., clothing traits except one, like “japanese clothes”) to focus the model on the intended concept. See example exclusion list ([Catbox](https://files.catbox.moe/2jbc93.txt)).

## Tools and Setup
- **Training Software**: Use the kohya_ss GUI ([GitHub](https://github.com/bmaltais/kohya_ss)) for a user-friendly interface. Install via Stability Matrix ([GitHub](https://github.com/LykosAI/StabilityMatrix)) for streamlined setup.
- **Hardware Requirements**: A minimum of 12GB VRAM is recommended, though 10GB is feasible with FP8 mixed precision. Training with 24GB VRAM allows for batch size=2, as noted in general SDXL LoRA guides ([Civitai](https://civitai.com/articles/1716/a-fresh-approach-to-sdxl-and-pony-xl-lora-training)).
- **Cloud Options**: For limited local resources, cloud platforms like RunPod can be used ([Medium](https://medium.com/@guillaume.bieler/training-stable-diffusion-in-the-cloud-using-runpod-and-kohya-ss-eaabd8f141b2)).

## Additional Considerations
- **Monitoring Training**: Check for overtraining (model reproduces training images exactly) or undertraining (poor concept generation). Adjust epochs or learning rate if needed. Saving models every 5–10 epochs allows for evaluation.
- **Style vs. Character LoRAs**: For character LoRAs, focus on consistent poses, angles, and lighting. For style LoRAs, a broader dataset (50–100 images) may be needed, potentially increasing network dim to 32.
- **Community Insights**: Parameters vary across use cases. For example, “Virtual 3d Diffusion Update” used 8160 steps and dim=16, suggesting higher steps for complex styles ([Civitai](https://civitai.com/models/532668)).
- **VRAM Optimization**: Gradient checkpointing and FP8 options are critical for low-VRAM setups, as noted in multiple sources ([Civitai](https://civitai.com/articles/1716/a-fresh-approach-to-sdxl-and-pony-xl-lora-training)).

## Citations
- [SDXL Pony Fast Training Guide](https://civitai.com/models/351583/sdxl-pony-fast-training-guide)
- [Training Preset JSON](https://files.catbox.moe/t5clrs.json)
- [General SDXL LoRA Training Guide](https://medium.com/@guillaume.bieler/a-comprehensive-guide-to-training-a-stable-diffusion-xl-lora-optimal-settings-dataset-building-844113a6d5b3)
- [Opinionated Guide to All LoRA Training](https://civitai.com/articles/1716/a-fresh-approach-to-sdxl-and-pony-xl-lora-training)
- [Pony Diffusion V6 XL](https://civitai.com/models/257749/pony-diffusion-v6-xl)

## Conclusion
Training a LoRA on Pony Diffusion V6 XL with the specified parameters offers a robust approach to achieving results similar to PonyXL. The combination of a low network rank, Prodigy optimizer, and a carefully curated dataset ensures efficient and high-quality adaptation. For alternative scenarios, such as training on the base SDXL model or adjusting for larger datasets, parameters like network dimension and epochs can be tweaked, but the provided settings serve as a reliable starting point for most character-focused LoRAs.
