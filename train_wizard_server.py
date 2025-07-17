"""Simple Gradio wizard for LoRA training."""

import os
import shutil
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
    """Extract the dataset, start training and optionally delete it."""

    dataset_path = _extract_dataset(dataset_zip, dest_dir)

    # Here you would normally call the real training command.
    status = (
        f"Training with dataset: {dataset_path}, model: {model_name}, lr:"
        f" {learning_rate}, batch: {batch_size}, rank: {rank}."
    )

    if delete_after:
        shutil.rmtree(dataset_path)
        status += " Dataset deleted after training."

    return status

with gr.Blocks() as wizard:
    gr.Markdown("## LoRA Training Wizard")

    dataset_zip = gr.File(label="Upload Zipped Dataset", file_types=[".zip"])
    dest_dir = gr.Textbox(
        label="Extract To", value="datasets", placeholder="Destination folder"
    )
    delete_after = gr.Checkbox(label="Delete dataset after training", value=False)
    preset_choice = gr.Dropdown(label="Preset", choices=list(PRESETS.keys()), value="SD1.5")
    model = gr.Textbox(label="Base Model")
    learning_rate = gr.Textbox(label="Learning Rate")
    batch_size = gr.Textbox(label="Batch Size")
    rank = gr.Textbox(label="Network Rank")

    preset_choice.change(
        apply_preset,
        inputs=preset_choice,
        outputs=[model, learning_rate, batch_size, rank],
    )

    begin_button = gr.Button("Begin Training")
    status = gr.Textbox(label="Status")
    begin_button.click(
        start_training,
        inputs=[dataset_zip, dest_dir, delete_after, model, learning_rate, batch_size, rank],
        outputs=status,
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    wizard.launch(server_name=host, share=False)
