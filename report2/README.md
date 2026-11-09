# Report 2 — Practical Spectral Subtraction

This directory contains the MATLAB implementation, final report, and saved experimental results for ELEC5305 Report 2.

## Files

- `Report2 ChenxinZhang.mlx` — main MATLAB Live Script.
- `Report2 ChenxinZhang.pdf` — final written report.
- `r2_*.m` — supporting MATLAB functions.
- `results/` — saved experimental measurements.
- `validation_data/` — input manifest, source information, checksums, and licensing information.

## Running the experiment

Open `Report2 ChenxinZhang.mlx` in MATLAB with this directory as the Current Folder.

Full recomputation requires the original `clean_speech.wav`, `car_idle_noise.mp3`, and the validation audio files referenced by `validation_data/speech_manifest.csv` and `r2_validation_prepare.m`.

Audio files are not included in this repository. Consult `validation_data/DATA_SOURCES.txt` for their sources and preparation details.

The existing results can be inspected in `results/` without rerunning the experiment.
