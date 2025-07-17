"""Simple Gradio wizard for LoRA training."""

import os
import shutil
import time
import zipfile

import gradio as gr

# Recommended parameter presets derived from the markdown reports in ``info/``.
PRESETS = {
    "SD1.5": {
        "base_model": "runwayml/stable-diffusion-v1-5",
        "learning_rate": "1e-4",
        "batch_size": "2",
        "rank": "32",
    },
    "SDXL": {
        "base_model": "stabilityai/stable-diffusion-xl-base-1.0",
        "learning_rate": "3e-5",
        "batch_size": "1",
        "rank": "64",
    },
    "PonyXL": {
        "base_model": "civitai/pony-diffusion-v6-xl",
        "learning_rate": "1.0",
        "batch_size": "3",
        "rank": "16",
    },
}


def predict_vram(batch_size: str, rank: str) -> str:
    """Return an estimated VRAM usage string for the given settings."""
    try:
        bs = int(batch_size)
        rk = int(rank)
    except (ValueError, TypeError):
        return "Estimated VRAM: N/A"

    base_mb = 2000
    mem_mb = base_mb + bs * 500 + rk * 20
    return f"Estimated VRAM: {mem_mb / 1024:.1f} GB"


def _extract_dataset(zip_file: str, dest_dir: str) -> str:
    """Extract ``zip_file`` to ``dest_dir`` and return the dataset path."""
    base_name = os.path.splitext(os.path.basename(zip_file))[0]
    dataset_path = os.path.join(dest_dir, base_name)
    os.makedirs(dataset_path, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as archive:
        archive.extractall(dataset_path)
    return dataset_path


def apply_preset(preset_name: str) -> tuple[str, str, str, str]:
    """Return parameter defaults for the given preset."""
    preset = PRESETS.get(preset_name, {})
    return (
        preset.get("base_model", ""),
        preset.get("learning_rate", ""),
        preset.get("batch_size", ""),
        preset.get("rank", ""),
    )


def start_training(
    dataset_zip: str,
    dest_dir: str,
    delete_after: bool,
    model_name: str,
    learning_rate: str,
    batch_size: str,
    rank: str,

) -> str:
    """Extract the dataset, simulate training, and optionally delete it."""

    dataset_path = _extract_dataset(dataset_zip, dest_dir)

    epochs = 3
    steps_per_epoch = 5
    for epoch in range(1, epochs + 1):
        for step in range(1, steps_per_epoch + 1):
            yield f"Epoch {epoch}/{epochs} Step {step}/{steps_per_epoch}"
            time.sleep(0.1)

    status = (
        f"Training with dataset: {dataset_path}, model: {model_name}, lr:"
        f" {learning_rate}, batch: {batch_size}, rank: {rank}."
    )

    if delete_after:
        shutil.rmtree(dataset_path)
        status += " Dataset deleted after training."

    yield status

with gr.Blocks() as wizard:
    gr.Markdown("# LoRA Training Wizard\nUpload a dataset and configure your run.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Dataset")
            dataset_zip = gr.File(
                label="Zipped Dataset", file_types=[".zip"], file_count="single"
            )
            dest_dir = gr.Textbox(
                label="Extract To", value="datasets", placeholder="Destination folder"
            )
            delete_after = gr.Checkbox(
                label="Delete dataset after training", value=False
            )

        with gr.Column():
            gr.Markdown("### Training Settings")
            preset_choice = gr.Dropdown(
                label="Preset", choices=list(PRESETS.keys()), value="SD1.5"
            )
            model = gr.Textbox(label="Base Model")
            learning_rate = gr.Textbox(label="Learning Rate")
            batch_size = gr.Textbox(label="Batch Size")
            rank = gr.Textbox(label="Network Rank")

    with gr.Row():
        vram_info = gr.Markdown(predict_vram("2", "32"))

    preset_choice.change(
        apply_preset,
        inputs=preset_choice,
        outputs=[model, learning_rate, batch_size, rank],
    ).then(
        predict_vram,
        inputs=[batch_size, rank],
        outputs=vram_info,
    )

    batch_size.change(predict_vram, inputs=[batch_size, rank], outputs=vram_info)
    rank.change(predict_vram, inputs=[batch_size, rank], outputs=vram_info)

    with gr.Row():
        begin_button = gr.Button("Begin Training")
        status = gr.Textbox(label="Status", interactive=False)
    begin_button.click(
        start_training,
        inputs=[dataset_zip, dest_dir, delete_after, model, learning_rate, batch_size, rank],
        outputs=status,
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    wizard.launch(server_name=host, share=False)
