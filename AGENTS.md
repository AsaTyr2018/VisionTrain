# AGENT guidelines
This repository hosts training scripts and resources for building LoRA (Low Rank Adaptation) models for various Stable Diffusion variants including SD 1.5, SDXL, and the community fork PonyXL.

## Scope
- Datasets can be sourced from [Hugging Face](https://huggingface.co/) and [Civitai](https://civitai.com/), ensuring license compliance for all assets.
- Training is targeted at LoRA adapters for image generation using the diffusers library or other Stable Diffusion tooling (e.g. kohya-ss / sd-scripts). The repo will contain scripts and configuration examples.
- Primary focus is on SD 1.5 and SDXL, with additional experiments for the derivative PonyXL.

## Development Guidelines
1. **Environment**
   - Use Python 3.10+ with GPU support (CUDA 11+). Recommended packages include `diffusers`, `transformers`, `accelerate`, and `bitsandbytes` for efficient LoRA training.
   - When adding new Python code, follow PEP8 style guidelines. Use descriptive variable names and docstrings for functions/classes.
2. **Training Plan**
   - Prepare datasets with high-quality images and text captions. Consider using libraries like `datasets` or custom dataloaders.
   - Example command to train a LoRA with diffusers:
     ```bash
     accelerate launch train_text_to_image_lora.py \
       --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
       --dataset_name="<dataset_path>" \
       --resolution=512 --train_batch_size=1 \
       --gradient_accumulation_steps=4 --num_train_epochs=10 \
       --learning_rate=1e-4 --report_to="tensorboard" 
     ```
   - Adjust parameters for SDXL or PonyXL accordingly (e.g., `--pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0"`).
3. **Testing**
   - Validate LoRA checkpoints by running sample image generation using `diffusers` pipelines.
   - Provide example notebooks or scripts demonstrating usage.

## Documentation
- Update `README.md` with instructions for new scripts and experiments.
- Document dataset sources and licensing considerations.
- Keep track of findings or hyperparameters in dedicated markdown files under a `docs/` directory.

## Programmatic Checks
- If tests or linters are added (e.g., `pytest`, `flake8`), ensure they run successfully before committing.
- Future scripts should include a simple CLI or notebook for reproducibility.

