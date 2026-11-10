# When Better Denoising Does Not Mean Better Speaker Verification: An Empirical Study of Speech Enhancement and Speaker Identity Preservation

Chenxin Zhang · ELEC5305 Speech and Audio Processing · University of Sydney

## Overview

This project investigates why improvements in speech enhancement do not always translate into better speaker verification. It combines student-developed MATLAB spectral subtraction, pretrained DeepFilterNet3, and a fixed SpeechBrain ECAPA-TDNN verifier to examine how signal quality, subtraction strength and noise conditions relate to speaker identity.

The main experiment has been executed, and its formal results have been checked against the final report. The added clean-query experiment has also been recomputed and independently checked. **[final_project.mlx](final_project.mlx) is the single main Run All entry point**, with saved outputs and English analysis throughout its 26 sections.

## Implementation and experiment

The student-developed MATLAB code implements STFT analysis, weighted overlap-add reconstruction, percentile and simplified VAD noise estimation, power-domain spectral subtraction, and speech/noise component decomposition. Analysis uses 16 kHz audio, a 32 ms periodic Hann window, an 8 ms hop and a 1024-point FFT. The default subtraction strength is α=1.5 and the power floor is β=0.02.

The MATLAB local functions are in the notebook's final appendix. Python scripts prepare the fixed inputs and call the external models. VOICEBOX supplies the tracking noise estimator and an implementation comparison. DeepFilterNet3 and ECAPA are used without training or fine-tuning; ECAPA produces 192-dimensional embeddings for cosine scoring.

Development contains **624 mixtures**. The formal test contains **1080 mixtures**, using 20 enrolled speakers, 10 external test speakers, nine noise sources and SNRs of −5, 0, 5 and 10 dB. The noise groups are relatively low-variation environments, high-variation environments and four-reader babble. Development and testing use separate source recordings, noise sources and external-speaker groups; the enrolled speakers are shared.

## Verified findings

Quality means use the **720 enrolled-speaker test mixtures**. External-verification EER uses **720 genuine and 7200 external-impostor comparisons** per method, with the primary enrollment references. SI-SDR gain and STOI change are relative to Noisy; lower EER is better.

| Method | Mean SI-SDR gain (dB) | Mean STOI change | External EER (%) |
|---|---:|---:|---:|
| Noisy | 0.000 | 0.0000 | 7.083 |
| Percentile spectral subtraction, α=1.5 | +0.929 | -0.0037 | 8.764 |
| Tracking spectral subtraction | +1.167 | +0.0016 | 7.639 |
| DeepFilterNet3 | +6.258 | +0.0291 | 9.028 |

DeepFilterNet3 improves SI-SDR and STOI but has a higher EER than Noisy. Default percentile subtraction improves SI-SDR while slightly reducing STOI, and also increases EER. These results demonstrate the importance of evaluating speech enhancement against its downstream verification task, rather than relying on signal-quality metrics alone.

Development selected **α=3** for mean SI-SDR gain and **α=0.5** for external-verification EER. The common Noisy development decision threshold is approximately **0.270079**. EER uses the score distribution; BER evaluates errors at a fixed decision threshold. Paired speaker-cluster bootstrap analysis uses 20,000 resamples.

See the [test summary](results/tables/test/test_summary.csv), [development selection](results/tables/development/development_selection.csv), [primary comparisons](results/tables/test/primary_comparisons.csv) and [α analysis figure](results/figures/alpha_analysis.pdf).

## Repository structure

```text
final_project.mlx              Complete stepwise experiment and local MATLAB functions
src/scripts/                   Batch input preparation and external-model adapters
src/materials/                 Deterministic data preparation scripts
src/matlab/                    MATLAB layout and standalone clean-query reproduction helpers
protocol/                      Fixed settings, manifests, model identities and requirements
runtime.local.example.json     Template for private local configuration
results/tables/development/    Development metrics, thresholds and parameter selection
results/tables/test/           Test metrics, comparisons, cases and robustness results
results/figures/               Main-report and clean-query figures
results/report/                Report reconstruction scripts, numerical inputs and insertable clean-query section
docs/                          Setup, provenance and third-party notices
requirements-inspection.txt    Lightweight Python inspection/plotting requirements
.gitignore                     Excludes private settings and generated material
```

The retained `src/matlab/` directory supports a historical directory link created by the Python initializer. The MATLAB implementations themselves are local functions in the MLX. See [code and data provenance](docs/CODE_AND_DATA_PROVENANCE.md).

## Requirements and setup

Full Run All requires **separately obtained datasets, models and external tools**. The validated environment uses:

- MATLAB **R2025b**, Signal Processing Toolbox and Audio Toolbox.
- Python **3.12**, with versions recorded in [protocol/requirements.lock.txt](protocol/requirements.lock.txt).
- Apple-silicon macOS for the fixed **DeepFilterNet v0.5.6** executable and the existing POSIX shell/symlink adapters.
- The pinned DeepFilterNet3 ONNX archive, SpeechBrain ECAPA model files and VOICEBOX revision.
- LibriSpeech test-clean/dev-clean, the specified DEMAND recordings and the fixed babble sources.

Follow [data and model setup](docs/DATA_AND_MODELS.md) for the exact directory layout, sources and revisions. To create the full Python environment from the project root:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r protocol/requirements.lock.txt
cp runtime.local.example.json runtime.local.json
```

Edit the three fields in `runtime.local.json`:

| Field | Set it to |
|---|---|
| `python` | The intended Python executable, for example `.venv/bin/python` after the setup above |
| `materials_root` | The directory containing `material_audit/` and `noise_audit/` in the documented layout |
| `tools_root` | The directory containing the fixed DeepFilterNet executable/archive, `ecapa_model/` and `voicebox_source/` |

Paths may be absolute or relative to the project root. Use actual local locations; the supplied example is a layout template. Keep `runtime.local.json` private and excluded from Git.

## Run or inspect the experiment

### Complete recomputation

1. Obtain the materials and tools, install the dependencies and configure `runtime.local.json`.
2. Set MATLAB **Current Folder** to this project directory.
3. Open **`final_project.mlx`** and click **Run All**.
4. After completion, inspect the outputs and save the Live Script.

Sections 1–11 explain the DSP on a fixed example; Sections 12–14 generate development data and select parameters; Sections 15–24 process test data and present the main analyses. Section 25 adds the clean-query reference and clean-input enhancement checks; Section 26 summarizes the findings. Each section retains its code, results and interpretation. Each Run All creates a new `runs/experiment_en_*` directory and recomputes the main experiment and the clean-query checks. It does not automatically reuse previous results.

A run generates input audio, traditional and DeepFilterNet outputs, embeddings and scores, development selections, test summaries, case analyses, bootstrap results, diagnostic files and logs. The completed run is marked by `stepwise_completed.mat`. Batch progress and warnings are written to that run's logs. Full recomputation requires processing time and disk space.

### Inspect included results without model inference

Open the MLX to read its saved tables and figures without clicking Run All. The [included result tables](results/tables/) and [report figures](results/figures/) remain available without model inference. To check the recorded clean-query scores in MATLAB, clear the workspace and execute only Section 25; it recalculates the metrics and draws the score distributions from saved numerical data. This does not need Python, source audio or model weights.

For optional report figure/table reconstruction from the included numerical inputs:

```sh
python3.12 -m venv .venv-inspect
.venv-inspect/bin/python -m pip install -r requirements-inspection.txt
.venv-inspect/bin/python results/report/scripts/make_figures.py
.venv-inspect/bin/python results/report/scripts/make_tables.py
```

These scripts regenerate plots and LaTeX table bodies under `results/report/`; they do not rerun enhancement or speaker verification. Published files exclude run directories, source/generated audio, model weights, private configuration and virtual environments. A completed local `runs/` directory may remain on the author's computer but is ignored by Git.

## Data and external software attribution

- **LibriSpeech:** V. Panayotov, G. Chen, D. Povey and S. Khudanpur; [OpenSLR corpus](https://www.openslr.org/12/), CC BY 4.0. Also supplies the readers used to construct babble.
- **DEMAND:** J. Thiemann, N. Ito and E. Vincent; [official dataset record](https://zenodo.org/records/1227121).
- **VOICEBOX:** Mike Brookes / Imperial College London; [speech-processing toolbox](https://github.com/ImperialCollegeLondon/sap-voicebox), used for tracking noise estimation and implementation comparison.
- **SpeechBrain / ECAPA-TDNN:** [pretrained speaker model](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb); ECAPA-TDNN by B. Desplanques, J. Thienpondt and K. Demuynck.
- **DeepFilterNet3:** H. Schröter and colleagues; [DeepFilterNet project](https://github.com/Rikorose/DeepFilterNet), using the fixed executable and model described above.

Dataset sources, licensing information and third-party software acknowledgements are documented in the [third-party notices](docs/THIRD_PARTY_NOTICES.md) and [source and license audit](protocol/SOURCE_AND_LICENSE.md). Original dataset audio is not redistributed.

## Clean-query reference integrated into the main project

Open `final_project.mlx`: Section 25 contains the supplementary check and Section 26 contains the final summary. The existing main results remain unchanged. Clean EER is 0.000%; default SS and DeepFilterNet give 0.167% and 0.000%. At the unchanged development threshold, BER is 1.250%, 2.000% and 1.500%, respectively. Each clean condition uses 60 genuine and 600 external trials.

- Results and trial scores: [results/tables/clean_query](results/tables/clean_query/)
- Provenance and validation: [results/audits/clean_query](results/audits/clean_query/)
- Method and reproduction: [docs/CLEAN_QUERY_EXPERIMENT.md](docs/CLEAN_QUERY_EXPERIMENT.md)
- Recording sequence: [docs/VIDEO_ADDENDUM.md](docs/VIDEO_ADDENDUM.md)
- Insertable report fragment: [results/report/sections/clean_query.tex](results/report/sections/clean_query.tex)

Full Run All runs fresh clean-query inference for the current experiment. To inspect the recorded clean results without inference, clear the MATLAB workspace and run only Section 25, or read its saved output. The redundant standalone clean-query notebook and the previous main copies are archived outside this active project; see the merge receipt for their backup paths.
