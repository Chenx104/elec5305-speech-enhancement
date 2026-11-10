# Data Sources and Third-Party Software

This project uses public speech datasets, established speech-processing software and pretrained models. The MATLAB spectral-subtraction implementation and experiment analysis are described separately in [Code and Data Provenance](CODE_AND_DATA_PROVENANCE.md).

## Speech and noise datasets

**LibriSpeech**  
V. Panayotov, G. Chen, D. Povey and S. Khudanpur, “LibriSpeech: An ASR Corpus Based on Public Domain Audio Books,” *ICASSP*, 2015.  
[OpenSLR dataset page](https://www.openslr.org/12/) · License listed by OpenSLR: **CC BY 4.0**.  
The project uses `test-clean` and `dev-clean` for speaker enrollment, development, testing and babble-source construction.

**DEMAND (Diverse Environments Multi-channel Acoustic Noise Database)**  
J. Thiemann, N. Ito and E. Vincent, “DEMAND: A Collection of Multi-Channel Recordings of Acoustic Noise in Diverse Environments,” 2013.  
[Zenodo dataset record](https://zenodo.org/records/1227121).  
The study uses selected environmental recordings from channel 1. The Zenodo metadata and accompanying dataset documentation contain different Creative Commons license indications; the recorded sources are documented in [`protocol/SOURCE_AND_LICENSE.md`](../protocol/SOURCE_AND_LICENSE.md).

**Four-reader babble**  
Constructed from specified LibriSpeech recordings, with speaker groups and generation rules defined in the project protocol. LibriSpeech attribution applies to its source audio.

## Enhancement and verification software

**DeepFilterNet3**  
H. Schröter, T. Rosenkranz, A. N. Escalante-B. and A. Maier, “DeepFilterNet: Perceptually Motivated Real-Time Speech Enhancement,” 2023.  
[Source repository](https://github.com/Rikorose/DeepFilterNet) · [v0.5.6 release](https://github.com/Rikorose/DeepFilterNet/releases/tag/v0.5.6).  
The experiment uses the specified DeepFilterNet3 model with the external executable; model weights are not part of this repository. Source license files are retained under `protocol/DeepFilterNet_LICENSE*.txt`.

**SpeechBrain ECAPA-TDNN**  
B. Desplanques, J. Thienpondt and K. Demuynck, “ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification,” *Interspeech*, 2020.  
[Pretrained SpeechBrain model](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) · [Selected model revision](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/tree/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286).  
The model card lists **Apache-2.0**. The project uses pretrained embeddings and cosine-score verification without model fine-tuning.

**VOICEBOX**  
Mike Brookes / Imperial College London.  
[Source repository](https://github.com/ImperialCollegeLondon/sap-voicebox) · [Selected revision](https://github.com/ImperialCollegeLondon/sap-voicebox/tree/a8916a8e87294ebd052b91a1f50e196351b3e561).  
Used for minimum-statistics noise estimation and an independent spectral-subtraction comparison. Function-level notices identify LGPL-3.0-or-later licensing.

## Additional dependencies and distribution

MATLAB and its toolboxes are separately licensed software. Python dependencies and versions are specified in [`protocol/requirements.lock.txt`](../protocol/requirements.lock.txt).

The repository contains project code, configurations, metrics and analysis figures. It does not include source or generated speech recordings, external model weights or external executable binaries. Dataset and software access remains subject to the terms supplied by their respective publishers.
