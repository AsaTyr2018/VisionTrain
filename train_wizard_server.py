"""Simple Gradio wizard for LoRA training."""

import os
import shutil
import zipfile

import gradio as gr


def _extract_dataset(zip_file: str, dest_dir: str) -> str:
    """Extract ``zip_file`` to ``dest_dir`` and return the dataset path."""
    base_name = os.path.splitext(os.path.basename(zip_file))[0]
    dataset_path = os.path.join(dest_dir, base_name)
    os.makedirs(dataset_path, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as archive:
        archive.extractall(dataset_path)
    return dataset_path


def start_training(
    dataset_zip: str,
    dest_dir: str,
    delete_after: bool,
    model_name: str,
) -> str:
    """Extract the dataset, start training and optionally delete it."""

    dataset_path = _extract_dataset(dataset_zip, dest_dir)

    # Here you would normally call the real training command.
    status = (
        f"Training would start with dataset: {dataset_path}, model: {model_name}."
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
    model = gr.Textbox(
        label="Base Model",
        placeholder="e.g. runwayml/stable-diffusion-v1-5",
    )

    begin_button = gr.Button("Begin Training")
    status = gr.Textbox(label="Status")
    begin_button.click(
        start_training,
        inputs=[dataset_zip, dest_dir, delete_after, model],
        outputs=status,
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    wizard.launch(server_name=host, share=False)
