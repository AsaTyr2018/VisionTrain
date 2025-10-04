# VisionTrain Training Wizard Project Plan

## Vision and Goals
- Deliver an easy-to-use training experience focused on Low-Rank Adaptation (LoRA) for Stable Diffusion text-to-image models.
- Embrace a modern, compact interface built with the latest Gradio components and a guided wizard-style workflow.
- Support the core training domains: SD1.5, SDXL, PonyXL, and Illustration-focused fine-tuning.
- Provide a responsive, self-service tool that handles base-model acquisition and exposes training control at the right depth for each user mode.

## Guiding Principles
1. **Simplicity first:** Surface only the essential decisions at each step while keeping defaults sensible and discoverable.
2. **Progressive disclosure:** Offer an "Easy" mode for quick starts and an "Advanced" mode for full parameter control.
3. **Responsiveness:** Communicate model downloads, validation, and training status with real-time feedback dialogs.
4. **Safety and reproducibility:** Capture user choices for auditability, reproducibility, and reruns.

## User Personas
| Persona | Needs | Wizard Mode Fit |
| --- | --- | --- |
| Hobbyist creator | Quick setup, curated defaults, minimal terminology. | Easy |
| Indie artist | Ability to tweak datasets, schedules, and logging while still guided. | Easy → Advanced |
| ML engineer | Full control over hyperparameters, resource allocation, and callbacks. | Advanced |

## Scope Overview
| Track | Description | Outcomes |
| --- | --- | --- |
| UX & Wizard Flow | Define screens, questions, and branching logic for Easy vs. Advanced. | Wireframes, interaction specs, copy guidelines. |
| Training Engine | Implement LoRA training pipelines for SD1.5, SDXL, PonyXL, and Illustration presets. | Modular training back-end with shared abstractions. |
| Model Handling | Automate downloading, caching, and selection of base models with download progress dialogs. | Reliable model registry and responsive UI feedback. |
| Platform & Ops | Package as a Gradio app with deployable configuration, logging, and monitoring. | Reproducible dev/prod setups. |
| Documentation & Support | Provide quick-start guides, FAQs, and onboarding flows. | Updated README and supporting docs. |

## Wizard Experience Blueprint
1. **Landing / Mode Selection**
   - Explain Easy vs. Advanced modes; remember last choice.
2. **Dataset Intake**
   - Questions about dataset location, format, and augmentation needs.
   - Easy mode uses presets (e.g., recommended captioning) while Advanced exposes batch size, shuffle, and validation split.
3. **Model & Objective Selection**
   - Options: SD1.5, SDXL, PonyXL, Illustration.
   - Auto-download base model with live progress dialog; allow manual path override in Advanced.
4. **Training Configuration**
   - Easy mode: learning rate, steps, and scheduler via guided choices with explanations.
   - Advanced: full hyperparameter matrix including optimizer, precision, LoRA rank, regularization prompts, and logging cadence.
5. **Resource Planning**
   - GPU selection, mixed precision toggles, gradient accumulation.
   - Easy mode sets defaults based on detected hardware.
6. **Review & Confirm**
   - Summarize all selections, highlight defaults, and allow edits.
7. **Run & Monitor**
   - Display training progress, ETA, and checkpoints.
   - Notify on model downloads, checkpoint saves, and completion.

## Technical Architecture
- **Frontend:** Gradio 4.x leveraging Blocks, Tabs, Accordions for compact layout; custom CSS for modern visual tone.
- **State Management:** Central wizard state object persisted per session; mode-aware validation for branching.
- **Training Backend:** Python services wrapping diffusers/LoRA tooling with pluggable configs per base model.
- **Model Registry:** YAML/JSON manifest describing supported models, source URLs, hashes, and default hyperparameters.
- **Download Service:** Async downloader with progress callbacks feeding UI dialogs.
- **Persistence:** Optional storage of runs, logs, and artifacts in a workspace directory with export support.

## Milestones & Deliverables
| Sprint | Focus | Key Deliverables |
| --- | --- | --- |
| 1 | Research & UX Foundations | Wireframes, copy draft, technical spikes for Gradio wizard patterns. |
| 2 | Wizard Skeleton & Model Registry | Mode selection flow, model manifest implementation, download progress dialog prototype. |
| 3 | Easy Mode Training Path | End-to-end Easy mode with SD1.5 preset; automated base-model download and training kickoff. |
| 4 | Advanced Mode Extensions | Full hyperparameter control, dataset fine-tuning options, validation hooks. |
| 5 | Additional Model Presets | SDXL, PonyXL, Illustration profiles with curated defaults and guidance text. |
| 6 | Polish & Launch Readiness | QA, documentation updates, telemetry hooks, packaging for deployment. |

## Risks & Mitigations
| Risk | Mitigation |
| --- | --- |
| Large model downloads impact UX. | Stream progress updates, allow resumable downloads, surface estimated times. |
| User confusion over parameters. | Provide contextual help tooltips, glossary links, and sensible defaults. |
| Hardware variability. | Detect GPU capabilities, offer fallbacks (CPU warnings), document requirements. |
| Maintenance burden for presets. | Centralize defaults in manifests and add automated checks for stale URLs. |

## Success Metrics
- Time-to-first-training run under 10 minutes for Easy mode users.
- 90% successful model download completion without manual intervention.
- User feedback rating of ≥4/5 for clarity and simplicity after pilot testing.
- Ability to re-run a saved configuration with identical outcomes.

## Next Steps
1. Validate requirements with stakeholders and incorporate feedback.
2. Prioritize sprint backlog, assign owners, and establish ceremonies.
3. Draft technical RFCs for training backend abstractions and downloader service.
4. Begin Sprint 1 activities per milestones.
