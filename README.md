# From SNR to Speaker Embeddings: Does Speech Enhancement Preserve Speaker Identity?

## Project Overview

This project investigates whether speech enhancement can improve signal quality while preserving speaker-identity information.

The project is being developed progressively through ELEC5305 Audio Processing Report 1, Audio Processing Report 2, and the final project.

In Report 1, a controlled STFT-based speech-enhancement pipeline was implemented in MATLAB using an oracle Wiener-style soft mask. This stage validated the main signal-processing pipeline, including controlled noise generation, FFT and STFT analysis, time-frequency masking, inverse FFT, overlap-add reconstruction, waveform and spectrogram comparison, and quantitative evaluation.

The next stage will extend this controlled baseline toward a practical noise-estimated spectral-subtraction system. Unlike the oracle experiment, the practical system will estimate noise information from the observed noisy speech rather than using the known clean speech and added noise.

Following Feedback 1, the final project has been revised from a general demonstration of STFT-based noise reduction to a broader research question: whether improvements in conventional speech-enhancement metrics also preserve speaker identity.

The student-developed classical STFT enhancement system will remain the main ELEC5305 signal-processing component. It will later be compared with a pretrained DeepFilterNet speech-enhancement model. Speaker-identity preservation will be evaluated using a frozen pretrained ECAPA-TDNN speaker-embedding model.

DeepFilterNet and ECAPA-TDNN will be used only as external pretrained reference and evaluation tools. They will not be presented as student-developed models.


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
