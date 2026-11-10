# When Better Denoising Does Not Mean Better Speaker Verification

**An Empirical Study of Speech Enhancement and Speaker Identity Preservation**  
ELEC5305 Speech and Audio Processing · The University of Sydney  
Chenxin Zhang

## About this project

Speech enhancement can make a recording sound clearer without making its speaker easier to verify. This project investigates that difference by comparing a MATLAB spectral-subtraction implementation with DeepFilterNet3, using a fixed ECAPA-TDNN speaker-verification model.

The experiments examine how enhancement strength, noise estimation and recording conditions affect both signal quality and speaker-verification errors. The MATLAB Live Script presents the processing steps, results and interpretation in one place.

## Main findings

The formal test includes **1,080 noisy mixtures** across nine noise sources and four input SNRs. Signal-quality averages use 720 target-speaker mixtures; verification uses separate clean enrolment recordings and external-impostor trials.

| Method | SI-SDR gain (dB) | STOI change | EER (%) |
| --- | ---: | ---: | ---: |
| Noisy | 0.000 | 0.0000 | 7.083 |
| Spectral subtraction (α = 1.5) | +0.929 | −0.0037 | 8.764 |
| Tracking spectral subtraction | +1.167 | +0.0016 | 7.639 |
| DeepFilterNet3 | +6.258 | +0.0291 | 9.028 |

DeepFilterNet3 achieves the largest improvements in SI-SDR and STOI, but its speaker-verification EER is higher than that of unprocessed noisy speech. Development experiments also select different subtraction strengths for signal quality (**α = 3**) and verification (**α = 0.5**).

A supplementary clean-query experiment compares unprocessed clean speech with speech enhanced without added noise. Clean-query EER is **0.000%**, compared with **0.167%** for default spectral subtraction and **0.000%** for DeepFilterNet3. At a common fixed threshold, BER is **1.250%**, **2.000%** and **1.500%**, respectively. These are descriptive results from 60 genuine and 600 external-impostor trials per condition.

**Key takeaway:** Better signal-quality scores do not necessarily mean better speaker-verification performance.

## Explore the project

- **[`final_project.mlx`](final_project.mlx)** — Main MATLAB Live Script, including the complete experiment and supplementary clean-query analysis (Sections 25–26).
- **[`final_project_preview.md`](final_project_preview.md)** — Read the Live Script's exported explanation, code and figures on GitHub.
- **[`results/figures/`](results/figures/)** — Main analysis figures and clean-query score distributions.
- **[`results/tables/`](results/tables/)** — Development, test and supplementary numerical results.
- **[`src/`](src/)** — MATLAB helpers and Python scripts for data preparation and model inference.
- **[`protocol/`](protocol/)** — Experiment configuration and fixed evaluation protocol.

## Reproduction and documentation

The project uses MATLAB R2025b, Python 3.12, LibriSpeech, DEMAND, VOICEBOX, DeepFilterNet3 and a pretrained SpeechBrain ECAPA-TDNN model. Datasets and pretrained model files are obtained separately and are not included in this repository.

For environment setup, file layout and reproduction instructions, see **[Data and Models](docs/DATA_AND_MODELS.md)**. For the supplementary experiment, see **[Clean-query Experiment](docs/CLEAN_QUERY_EXPERIMENT.md)**. Code ownership, sources and software acknowledgements are documented in **[Code and Data Provenance](docs/CODE_AND_DATA_PROVENANCE.md)** and **[Third-party Notices](docs/THIRD_PARTY_NOTICES.md)**.
