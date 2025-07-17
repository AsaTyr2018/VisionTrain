# VisionTrain
LoRA Training Appliance

## Gradio Wizard

A simple Gradio interface guides you through basic training options.

### Dataset Upload

You can upload a zipped dataset directly in the wizard. After selecting the ZIP
file, choose a destination folder for extraction (defaults to `datasets`). The
wizard extracts the archive and passes the extracted path to the training
command. Enable the checkbox to delete the extracted files automatically once
training finishes.

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

