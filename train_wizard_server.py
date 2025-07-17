import os
import gradio as gr


def start_training(dataset_path: str, model_name: str) -> str:
    """Return a status message for the selected training parameters."""
    status = f"Training would start with dataset: {dataset_path},"
    return f"{status} model: {model_name}"

with gr.Blocks() as wizard:
    gr.Markdown("## LoRA Training Wizard")
    dataset = gr.Textbox(label="Dataset Path", placeholder="Path to dataset")
    model = gr.Textbox(
        label="Base Model",
        placeholder="e.g. runwayml/stable-diffusion-v1-5",
    )
    begin_button = gr.Button("Begin Training")
    status = gr.Textbox(label="Status")
    begin_button.click(start_training, inputs=[dataset, model], outputs=status)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    wizard.launch(server_name=host, share=False)
