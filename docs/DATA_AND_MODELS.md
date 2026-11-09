# Obtain the fixed data and tools

No dataset or model downloads are executed by inspecting the repository. Paths below are relative to the package root. Full recomputation uses the original Apple-silicon macOS executable and POSIX shell/symlink handling; Windows and Linux are not drop-in supported platforms.

## 1. Python

Use Python 3.12. The included lock file records the original experiment environment, not a new installation tested on every operating system.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r protocol/requirements.lock.txt
```

Create `runtime.local.json` by copying `runtime.local.example.json`, and set `python` to `.venv/bin/python`, `materials_root` to `data/materials`, and `tools_root` to `tools`. Keep that local file out of Git. Use the JSON settings consistently: Python input initialization reads that file directly, so do not rely on environment-variable overrides alone.

## 2. Speech and fixed noise sources

Download the original **test-clean.tar.gz** and **dev-clean.tar.gz** from [LibriSpeech / OpenSLR 12](https://www.openslr.org/12/), leaving the archives compressed:

```text
data/materials/material_audit/test-clean.tar.gz
data/materials/material_audit/dev-clean.tar.gz
```

Create `data/materials/noise_audit` and copy:

- `protocol/A/material_audit/candidate_speaker_roles.csv` to `data/materials/material_audit/candidate_speaker_roles.csv`;
- the three `.py` scripts in `src/materials/` into `data/materials/noise_audit/`;
- `protocol/zenodo_record.json` into `data/materials/noise_audit/zenodo_record.json`.

Then run from the package root, in this order:

```sh
.venv/bin/python data/materials/noise_audit/fetch_channel01.py
.venv/bin/python data/materials/noise_audit/compute_variability.py
.venv/bin/python data/materials/noise_audit/build_babble_sources.py
```

These commands download DEMAND channel 1 and reconstruct the fixed five babble sources from the assigned readers. They require network access and disk space and were NOT executed during submission preparation. They retain the original seeds, reader groups, channel and resampling rules. Do not rerank/reassign the frozen manifests. WAV file headers may change, while decoded float32 samples must match the manifest's `DecodedFloat32SHA256`. The full experiment checks those sample hashes. The `Path` column in the packaged noise manifest is relative to `materials_root` and descriptive; runtime lookup uses SourceID and class.

Expected noise paths:

```text
data/materials/noise_audit/analysis16k/<SourceID>_ch01_16k.wav
data/materials/noise_audit/babble/<SourceID>.wav
```

## 3. Fixed tools and models

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

- Download the exact executable from [DeepFilterNet v0.5.6](https://github.com/Rikorose/DeepFilterNet/releases/tag/v0.5.6), and make it executable (`chmod +x tools/deep-filter-0.5.6-aarch64-apple-darwin`).
- Download [the pinned DeepFilterNet3 ONNX archive](https://github.com/Rikorose/DeepFilterNet/raw/978576aa8400552a4ce9730838c635aa30db5e61/models/DeepFilterNet3_onnx.tar.gz); retain the archive, do not substitute the current default model.
- Download the five files listed in `protocol/ecapa_model_revision.json` from [the pinned ECAPA revision](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/tree/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286). Copy that JSON to `tools/ecapa_model/model_revision.json`. Inference is offline, on CPU with four threads.
- Obtain [VOICEBOX at commit a8916a8e87294ebd052b91a1f50e196351b3e561](https://github.com/ImperialCollegeLondon/sap-voicebox/tree/a8916a8e87294ebd052b91a1f50e196351b3e561), preserving its license and notices. The code locates the `sap-voicebox-*` directory shown above.

The exact executable/model hashes remain in `protocol/reused_implementation_provenance.json`. Initialization checks the binary, DFN model archive and five ECAPA files. An equivalent model downloaded from a different revision is not a verified substitute. No training commands are needed.

## 4. Run

In MATLAB R2025b with Signal Processing Toolbox and Audio Toolbox, set Current Folder to this package, open `final_project.mlx`, and click Run All. Each run creates a new `runs/experiment_en_*` directory and recalculates development before testing. Sections 1–11 are the actual example; stop after Section 11 for an example-only demonstration. A complete Run All includes the full 624+1080 mixtures, external inference and 20,000 bootstrap resamples. No expensive run was performed in preparing this GitHub package.
