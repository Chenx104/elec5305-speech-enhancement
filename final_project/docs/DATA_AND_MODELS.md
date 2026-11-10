# Data and Model Setup

This guide describes the environment and input resources used to reproduce the MATLAB speech enhancement and speaker verification experiment. Commands are run from the `final_project/` directory.

## Software environment

The recorded configuration uses:

- **MATLAB R2025b**, with Signal Processing Toolbox and Audio Toolbox.
- **Python 3.12**, with the dependencies in [`protocol/requirements.lock.txt`](../protocol/requirements.lock.txt).
- **Apple-silicon macOS**, with the specified DeepFilterNet v0.5.6 executable and POSIX-compatible script interfaces.
- **VOICEBOX**, **DeepFilterNet3** and **SpeechBrain ECAPA-TDNN**, at the revisions listed below.

Create the Python environment:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r protocol/requirements.lock.txt
cp runtime.local.example.json runtime.local.json
```

Set the `python`, `materials_root` and `tools_root` fields in `runtime.local.json` to the corresponding paths. For the directory layout below, use `.venv/bin/python`, `data/materials` and `tools`. The runtime file is a local configuration and should not be committed.

## Speech datasets

Download the **LibriSpeech `test-clean` and `dev-clean` archives** from [OpenSLR 12](https://www.openslr.org/12/). Place the compressed archives at:

```text
data/materials/material_audit/test-clean.tar.gz
data/materials/material_audit/dev-clean.tar.gz
```

The protocol uses designated speakers and utterances for enrollment, development, testing, external impostors and babble generation. Speaker assignments and dataset manifests are recorded in `protocol/`.

## Environmental noise and babble

DEMAND recordings are obtained from the [DEMAND dataset](https://zenodo.org/records/1227121). The project uses channel 1, with noise-source selections and variability groups specified in its protocol files. Babble sources are constructed from four-reader LibriSpeech groups.

Prepare the expected material directory:

```text
data/materials/
  material_audit/
    test-clean.tar.gz
    dev-clean.tar.gz
    candidate_speaker_roles.csv
  noise_audit/
    fetch_channel01.py
    compute_variability.py
    build_babble_sources.py
    zenodo_record.json
```

Copy `protocol/A/material_audit/candidate_speaker_roles.csv` into `material_audit/`, copy the three scripts from `src/materials/` into `noise_audit/`, and copy `protocol/zenodo_record.json` to `noise_audit/`. Then run:

```sh
.venv/bin/python data/materials/noise_audit/fetch_channel01.py
.venv/bin/python data/materials/noise_audit/compute_variability.py
.venv/bin/python data/materials/noise_audit/build_babble_sources.py
```

Expected processed noise locations:

```text
data/materials/noise_audit/analysis16k/<SourceID>_ch01_16k.wav
data/materials/noise_audit/babble/<SourceID>.wav
```

The frozen manifests define the selected sources and allow decoded sample hashes to be checked. Use the recorded assignments for a comparable reproduction.

## Enhancement and verification models

Arrange the tools directory as follows:

```text
tools/
  deep-filter-0.5.6-aarch64-apple-darwin
  DeepFilterNet3_onnx.tar.gz
  ecapa_model/
    classifier.ckpt
    embedding_model.ckpt
    hyperparams.yaml
    label_encoder.txt
    mean_var_norm_emb.ckpt
    model_revision.json
  voicebox_source/
    sap-voicebox-a8916a8e87294ebd052b91a1f50e196351b3e561/
      voicebox/
```

**DeepFilterNet3.** Obtain the [v0.5.6 Apple-silicon executable](https://github.com/Rikorose/DeepFilterNet/releases/tag/v0.5.6) and the [specified ONNX model archive](https://github.com/Rikorose/DeepFilterNet/raw/978576aa8400552a4ce9730838c635aa30db5e61/models/DeepFilterNet3_onnx.tar.gz). Make the executable runnable:

```sh
chmod +x tools/deep-filter-0.5.6-aarch64-apple-darwin
```

**SpeechBrain ECAPA-TDNN.** Obtain the model files from [revision `0f99f2d0ebe89ac095bcc5903c4dd8f72b367286`](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/tree/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286). The required filenames are recorded in `protocol/ecapa_model_revision.json`; copy that record to `tools/ecapa_model/model_revision.json`.

**VOICEBOX.** Obtain [the specified VOICEBOX revision](https://github.com/ImperialCollegeLondon/sap-voicebox/tree/a8916a8e87294ebd052b91a1f50e196351b3e561) and retain its directory structure and notices.

Executable and model checksums are recorded in `protocol/reused_implementation_provenance.json`.

## MATLAB execution

1. Set MATLAB **Current Folder** to the `final_project/` directory.
2. Open `final_project.mlx`.
3. Review the saved outputs or select **Run All** for a complete recomputation.

Sections 1–11 demonstrate the DSP workflow; the subsequent sections prepare and evaluate the development and test sets, analyse results and perform clean-speech verification. The full run includes 624 development mixtures, 1,080 noisy test mixtures, model inference and speaker-cluster bootstrap evaluation. Output files are stored in a newly created `runs/experiment_en_*` directory.

For analysis without rerunning inference, use the saved Live Script outputs or browse the included [`results/`](../results/) directory. The [clean-speech analysis](CLEAN_QUERY_EXPERIMENT.md) also supports checking its recorded scores from MATLAB.
