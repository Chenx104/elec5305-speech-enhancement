# From SNR to Speaker Embeddings: Does Speech Enhancement Preserve Speaker Identity?

## Project Overview

This project investigates whether speech enhancement can improve signal quality while preserving speaker-identity information.

The project is being developed progressively through ELEC5305 Audio Processing Report 1, Audio Processing Report 2, and the final project.

In Report 1, a controlled STFT-based speech-enhancement pipeline was implemented in MATLAB using an oracle Wiener-style soft mask. This stage validated the main signal-processing pipeline, including controlled noise generation, FFT and STFT analysis, time-frequency masking, inverse FFT, overlap-add reconstruction, waveform and spectrogram comparison, and quantitative evaluation.

The next stage will extend this controlled baseline toward a practical noise-estimated spectral-subtraction system. Unlike the oracle experiment, the practical system will estimate noise information from the observed noisy speech rather than using the known clean speech and added noise.

Following Feedback 1, the final project has been revised from a general demonstration of STFT-based noise reduction to a broader research question: whether improvements in conventional speech-enhancement metrics also preserve speaker identity.

The student-implemented classical STFT enhancement pipeline will remain
the main ELEC5305 signal-processing component. It will later be compared
with a pretrained DeepFilterNet speech-enhancement model. Speaker-identity
preservation will be evaluated using a frozen pretrained ECAPA-TDNN
speaker-embedding model.

DeepFilterNet and ECAPA-TDNN are external pretrained tools. They will be
used only as a modern enhancement reference and a speaker-identity
evaluation tool, respectively, and will not be presented as
student-developed models.


## Revised Research Questions

**RQ1:** Does improvement in conventional speech-enhancement metrics correspond to preservation of speaker identity in a modern pretrained speaker-embedding model?

**RQ2:** How do classical STFT spectral subtraction and a modern neural enhancer trade noise reduction against speaker-identity preservation?


## Project Development / Progression

The project is structured as a progressive development from a controlled signal-processing experiment to a practical enhancement system and finally to a speaker-identity investigation.

### Stage 1 — Audio Processing Report 1: Controlled STFT Baseline

Clean speech  
↓  
Add controlled white Gaussian noise  
↓  
FFT / STFT analysis  
↓  
Oracle Wiener-style soft mask  
↓  
Inverse FFT  
↓  
Overlap-add reconstruction  
↓  
Enhanced speech  
↓  
SNR / RMS / ZCR / waveform / spectrogram evaluation

**Purpose:**  
Validate the complete STFT-based speech-enhancement and reconstruction pipeline under controlled conditions.

**Main limitation:**  
The oracle mask uses the known clean speech and added noise, so it is not a practical enhancement system.


### Stage 2 — Audio Processing Report 2: Practical Classical Enhancement

Noisy speech  
↓  
STFT  
↓  
Noise-spectrum estimation  
↓  
Spectral subtraction  
↓  
Spectral floor  
↓  
Inverse STFT  
↓  
Overlap-add reconstruction  
↓  
Enhanced speech  
↓  
Objective evaluation

**Purpose:**  
Replace the oracle baseline with a practical classical enhancement method that operates without access to the clean reference signal.

**Planned outcome:**  
A student-implemented noise-estimated spectral-subtraction system that can be used as the classical baseline in the final project.


### Stage 3 — Final Project: Speech Enhancement and Speaker Identity

Multi-speaker clean speech  
↓  
Add controlled environmental noise  
↓  
Noisy speech at multiple SNR conditions  
↓  

Classical spectral subtraction  
**versus**  
Pretrained DeepFilterNet  

↓  

Clean / Noisy / Classical Enhanced / Neural Enhanced speech  
↓  
Signal-quality evaluation: SNR / SI-SDR / STOI  
↓  
ECAPA-TDNN speaker embeddings  
↓  
Genuine and impostor speaker-verification scores  
↓  
Compare enhancement quality with speaker-identity preservation

**Final research objective:**  
Determine whether an enhancement method that produces better conventional signal-quality metrics also preserves speaker identity more effectively.

## Response to Feedback 1

Feedback 1 identified that the original project question focused mainly on whether STFT-based enhancement could reduce background noise. Although this is useful for demonstrating core DSP concepts, the basic effectiveness of classical speech enhancement is already well established.

In response, the project has been revised to investigate whether improvement in conventional speech-enhancement metrics also corresponds to preservation of speaker identity.

The classical STFT processing pipeline remains the main student-implemented ELEC5305 component. The current oracle-mask baseline will be extended to practical noise-estimated spectral subtraction. In the final project, this classical system will be compared with pretrained DeepFilterNet, while a frozen pretrained ECAPA-TDNN model will be used to evaluate speaker-identity preservation.

This revision shifts the project from simply asking whether noise can be reduced to investigating whether the enhancement process also preserves information about the person speaking.

## Work Completed to Date

Audio Processing Report 1 established the preliminary signal-processing baseline for the project.

The completed MATLAB implementation currently includes:

- loading and preprocessing clean speech;
- controlled white Gaussian noise generation;
- reproducible random-noise generation using fixed seeds;
- time-domain waveform analysis;
- FFT-based frequency-domain analysis;
- manual STFT frame processing;
- Hann windowing with 75% overlap;
- an oracle Wiener-style soft mask;
- inverse FFT reconstruction;
- overlap-add synthesis;
- clean, noisy, and enhanced waveform comparison;
- spectrogram comparison;
- SNR, RMS, and zero-crossing-rate evaluation;
- experiments at target input SNRs of 0 dB, 5 dB, and 10 dB;
- generation of clean, noisy, and enhanced WAV files.

### Report 1 Files

The complete preliminary MATLAB experiment is available below:

- [Report 1 MATLAB Live Script](./report1/Report1%20ChenxinZhang.mlx)
- [Report 1 PDF](./report1/Report1%20ChenxinZhang.pdf)
- [Clean speech](./report1/clean_speech.wav)
- [Noisy speech](./report1/noisy_speech.wav)
- [Enhanced speech](./report1/enhanced_speech.wav)

## Preliminary Results

The Report 1 oracle-mask experiment was evaluated under three controlled white-noise conditions.

| Target Input SNR | Measured Input SNR | Output SNR | SNR Improvement |
|---:|---:|---:|---:|
| 0 dB | 0.01 dB | 13.97 dB | 13.97 dB |
| 5 dB | 5.01 dB | 17.26 dB | 12.26 dB |
| 10 dB | 10.00 dB | 20.37 dB | 10.37 dB |

At the main 5 dB condition, the measured input SNR was approximately
5.01 dB, while the output SNR after enhancement was approximately
17.26 dB, corresponding to an improvement of approximately 12.26 dB.

The multi-SNR experiment also showed higher output SNR than input SNR under all three tested conditions.

These results demonstrate that the controlled noise-generation, STFT analysis, time-frequency masking, inverse transformation, overlap-add reconstruction, and evaluation pipeline are functioning as intended.

However, these results should be interpreted as validation of a controlled oracle baseline rather than the performance of a practical speech-enhancement system.

## Current Limitations

The preliminary experiment currently has several important limitations:

- only one speaker and one short speech segment have been evaluated;
- only white Gaussian noise has been tested;
- the oracle mask uses the known clean speech and added noise;
- the current evaluation focuses mainly on signal-level measures;
- speaker-identity preservation has not yet been evaluated.

The most important limitation is the oracle assumption. In a practical speech-enhancement system, the clean speech and exact added noise are not normally available. The next classical processing stage will therefore estimate the noise spectrum directly from the observed noisy speech.

These limitations motivate the progression toward practical spectral subtraction, multi-speaker evaluation, environmental noise, and speaker-embedding analysis.
