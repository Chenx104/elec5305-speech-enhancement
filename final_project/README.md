# When Better Denoising Does Not Mean Better Speaker Verification

**An Empirical Study of Speech Enhancement and Speaker Identity Preservation**  
Chenxin Zhang · ELEC5305 Speech and Audio Processing · The University of Sydney

## Overview

Speech enhancement can improve the quality of a recording without improving speaker verification. This project investigates that difference by comparing classical spectral subtraction with DeepFilterNet3 and evaluating both through a fixed ECAPA-TDNN speaker verification model.

The study examines how enhancement strength, noise estimation and input conditions influence signal quality, speech preservation and genuine–impostor score separation. Experiments cover noisy speech and clean-speech verification, with the full workflow presented in a 26-section MATLAB Live Script.

## Main results

The formal test includes 1,080 noisy speech mixtures across nine noise sources and four input SNRs (−5, 0, 5 and 10 dB). Signal-quality averages below use 720 target-speaker mixtures; speaker-verification EER uses 720 genuine and 7,200 external-impostor trials per method.

| Method | Mean SI-SDR gain (dB) | Mean STOI change | EER (%) |
|---|---:|---:|---:|
| Noisy | 0.000 | 0.0000 | 7.083 |
| Spectral subtraction (α = 1.5) | +0.929 | −0.0037 | 8.764 |
| Tracking spectral subtraction | +1.167 | +0.0016 | 7.639 |
| DeepFilterNet3 | +6.258 | +0.0291 | 9.028 |

DeepFilterNet3 achieves the largest improvements in SI-SDR and STOI, while speaker-verification EER is higher than for unprocessed noisy speech. Development-data selection also favours different subtraction strengths: **α = 3** for SI-SDR and **α = 0.5** for verification EER.

Clean-speech verification provides a reference for these findings. EER is **0.000%** for clean queries, **0.167%** after default spectral subtraction and **0.000%** after DeepFilterNet3. At the common development threshold, the corresponding balanced error rates are **1.250%**, **2.000%** and **1.500%**, respectively. These clean-condition rates come from 60 genuine and 600 external-impostor trials per method.

The central finding is that **better enhancement metrics do not necessarily produce better speaker verification**. Verification performance needs to be measured directly alongside signal quality.

## Explore the project

- **[MATLAB Live Script](final_project.mlx)** — complete experimental workflow, figures, results and MATLAB local functions.
- **[Readable MATLAB preview](final_project_preview.md)** — code, explanations and saved outputs in Markdown.
- **[Results](results/)** — verification metrics, signal-quality measurements, statistical comparisons and figures.
- **[Clean-speech verification](docs/CLEAN_QUERY_EXPERIMENT.md)** — protocol, results and associated analysis files.
- **[Data and model setup](docs/DATA_AND_MODELS.md)** — requirements and reproduction instructions.

## Project structure

```text
final_project.mlx            MATLAB experiment and analysis (26 sections)
final_project_preview.md     Markdown view of the Live Script
src/                         Python adapters, data preparation and MATLAB helpers
protocol/                    Experiment configuration and fixed dependencies
results/                     Tables, figures and analysis outputs
docs/                        Experiment, reproduction and attribution notes
runtime.local.example.json   Local configuration template
```

## Running the experiment

The workflow uses MATLAB R2025b with Signal Processing Toolbox and Audio Toolbox, Python 3.12, and the specified DeepFilterNet3, ECAPA-TDNN and VOICEBOX resources. The recorded full-run environment is Apple-silicon macOS.

To explore the work, open `final_project.mlx` and review its saved results. To recompute the experiment, follow [Data and Models](docs/DATA_AND_MODELS.md), configure `runtime.local.json` and run the Live Script from its project directory. Full execution includes data preparation, enhancement, embedding extraction and evaluation.

## Documentation and attribution

The MATLAB signal-processing implementation and evaluation workflow are documented in [Code and Data Provenance](docs/CODE_AND_DATA_PROVENANCE.md). External datasets, toolboxes and pretrained models are credited in [Third-Party Notices](docs/THIRD_PARTY_NOTICES.md).
