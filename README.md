# VisionTrain
LoRA Training Appliance

## Gradio Wizard

A simple Gradio interface guides you through basic training options. The form
is organized into two columns so dataset upload and training parameters are
clearly separated for a smoother workflow.

### Dataset Upload

You can upload a zipped dataset directly in the wizard. After selecting the ZIP
file, choose a destination folder for extraction (defaults to `datasets`). The
wizard extracts the archive and passes the extracted path to the training
command. Enable the checkbox to delete the extracted files automatically once
training finishes.

### Parameter Presets

Select a preset (SD1.5, SDXL, or PonyXL) to auto-fill recommended values for the
base model, learning rate, batch size, and network rank. These defaults are
derived from the markdown reports under the `info` directory.

### VRAM Estimate

An information box displays a rough VRAM estimate based on the current batch
size and network rank. The value updates whenever you change these settings or
select a new preset.

### Setup

Install all dependencies in a Python virtual environment:

```bash
bash setup.sh
```

### Launch

Start the wizard (the server listens on `0.0.0.0` for local network access):

```bash
bash start.sh
```

During training the status box now reports the current epoch and step.

