# Code and Data Provenance

## Project implementation

[`final_project.mlx`](../final_project.mlx) is the main experimental entry point. It contains the 26-section analysis and MATLAB local functions for short-time Fourier analysis and reconstruction, noise-spectrum estimation, power-domain spectral subtraction, speech/noise component decomposition, verification metrics and statistical evaluation.

Supporting code is organised as follows:

| Location | Role |
|---|---|
| `src/scripts/` | Python preparation, model adapters, embedding extraction and evaluation |
| `src/materials/` | Reproducible speech and noise material preparation |
| `src/matlab/clean_query/` | MATLAB functions for clean-speech analysis |
| `src/scripts/clean_query/` | Clean-speech data preparation and verification analysis |
| `protocol/` | Experiment settings, dataset manifests, dependency versions and model identifiers |
| `results/` | Numeric results, statistical comparisons, figures and analysis records |

The MATLAB spectral-subtraction and signal-analysis components are project implementations. The pretrained DeepFilterNet3 and SpeechBrain ECAPA-TDNN models provide external enhancement and speaker-representation methods; VOICEBOX contributes minimum-statistics tracking and an implementation comparison. Their original authors and software sources are listed in [Third-Party Notices](THIRD_PARTY_NOTICES.md).

## Data and evaluation design

Speech comes from LibriSpeech `test-clean` and `dev-clean`. Noise includes selected DEMAND recordings and four-reader babble constructed from the designated LibriSpeech speakers. The formal experiment comprises **624 development mixtures** and **1,080 test mixtures**, evaluated at −5, 0, 5 and 10 dB. The 20 enrolled speakers share identities across development and test, with separate enrollment, development and test utterances. External speakers and noise sources follow the recorded development/test partition.

Development determines subtraction-strength selection and verification thresholds. Formal test scores are computed with those choices fixed. The principal test uses 720 genuine and 7,200 external-impostor comparisons per method. The clean-speech verification analysis uses 60 genuine and 600 external-impostor trials per condition; its procedure and results are documented in [Clean-Speech Verification Analysis](CLEAN_QUERY_EXPERIMENT.md).

The fixed protocol, seeds, selected material identifiers and dependency versions are stored under `protocol/`. Numerical results and verification scores are available under `results/tables/`; report figures and analysis records are under `results/figures/` and `results/audits/`.

## Reproducibility

A full recomputation uses the data sources, versions and model revisions described in [Data and Models](DATA_AND_MODELS.md). The repository contains the code, experimental specifications and reported numerical outputs. Original corpus recordings, generated audio, model weights, local run directories and machine-specific runtime settings are not part of the repository.

The published results can be inspected directly in the saved MATLAB Live Script, Markdown preview and result tables. New runs create their own experiment outputs and use the defined development selection and evaluation procedures.
