# Project Proposal: STFT-Based Speech Enhancement

## 1. Project Title

STFT-Based Speech Enhancement

## 2. Student Information

- Full Name: Chenxin Zhang
- Student ID (SID): 540881826
- GitHub Username: Chenx104
- GitHub Project Link: https://github.com/Chenx104/elec5305-speech-enhancement

## 3. Project Overview

This project aims to develop and evaluate a speech enhancement method for noisy audio signals using short-time Fourier transform (STFT) based processing. Speech recordings in real environments are often affected by background noise from traffic, fans, rooms, or other acoustic sources. This noise can reduce speech intelligibility and make further audio analysis more difficult. The proposed project will investigate how noisy speech can be represented in the time-frequency domain and how frequency-domain noise reduction can improve the quality of the signal.

The main idea is to start with a clean speech recording, generate a noisy speech signal by adding controlled background noise, and then apply an STFT-based enhancement algorithm. The noisy signal will be divided into short overlapping frames, multiplied by a window function, and transformed into the frequency domain using the fast Fourier transform (FFT). A spectral subtraction method will then be applied to reduce the estimated noise magnitude in each frequency bin. Finally, the enhanced speech will be reconstructed using inverse STFT and overlap-add.

## 4. Background and Motivation

Speech enhancement is an important application of audio signal processing. It is used in mobile communication, hearing aids, online meetings, automatic speech recognition, and audio restoration. In many practical situations, the desired speech signal is mixed with unwanted background noise. Since speech is non-stationary, its frequency content changes over time. A single Fourier transform can show which frequencies exist in the whole signal, but it does not show when those frequencies occur. Therefore, STFT is a suitable tool because it provides a time-frequency representation of the speech signal.

This project is strongly connected to the concepts studied in ELEC5305. Sampling rate and aliasing are relevant when reading and processing digital audio signals. The DFT and FFT are used to analyse frequency content. Windowing and overlapping frames are central to STFT analysis. Inverse STFT and overlap-add reconstruction are needed to convert the processed frequency-domain signal back into the time domain. Audio features such as RMS energy, zero-crossing rate, and spectral centroid can also be used to compare the noisy and enhanced speech.

## 5. Proposed Methodology

The project will be implemented in MATLAB. First, a short clean speech recording will be selected or recorded. The audio signal will be converted to mono if necessary and resampled to a suitable sampling rate such as 16 kHz or 22.05 kHz. A noisy version of the speech will be created by adding white noise or recorded background noise at a controlled signal-to-noise ratio.

The clean, noisy, and enhanced signals will be analysed in both the time and frequency domains. Waveform plots will show the amplitude variation over time, while FFT-based spectra will show the frequency content. Spectrograms will be generated using STFT to show how the frequency content changes over time.

For enhancement, the noisy speech will be processed frame by frame. A window function such as a Hann or square-root Hann window will be applied to each frame. The FFT will transform each frame into the frequency domain. The noise spectrum will be estimated from a noise-only segment or from low-energy frames. Spectral subtraction will then reduce the estimated noise magnitude from the noisy speech magnitude spectrum. The phase of the noisy speech will be kept for reconstruction. The enhanced frames will be transformed back to the time domain using inverse FFT and reconstructed using overlap-add.

The performance will be evaluated by comparing the noisy and enhanced signals. If the clean reference signal is available, signal-to-noise ratio improvement will be calculated. Audio features such as RMS energy, zero-crossing rate, and spectral centroid will also be compared to observe how the enhancement changes the signal characteristics.

## 6. Expected Outcomes

The expected outcome is a MATLAB-based speech enhancement system that demonstrates the use of STFT and spectral subtraction for noisy speech signals. The project should produce waveform plots, frequency spectra, and spectrograms for the clean, noisy, and enhanced speech signals. It should also provide a basic quantitative evaluation using SNR improvement and selected audio features.

The final result is expected to show that STFT-based processing can reduce background noise while preserving the main speech structure. Even if the enhancement is not perfect, the project will demonstrate the practical use of sampling, FFT, windowing, STFT, overlap-add reconstruction, filtering ideas, and audio feature analysis from the course.

## 7. Timeline

| Week | Task |
|---|---|
| 1-2 | Select project topic and create GitHub project site |
| 3-5 | Review speech enhancement, STFT, spectral subtraction, and audio feature literature |
| 6-7 | Prepare clean and noisy speech data |
| 8-9 | Implement STFT analysis and spectrogram visualisation in MATLAB |
| 10 | Implement spectral subtraction and inverse STFT reconstruction |
| 11 | Evaluate results using SNR and audio features |
| 12-13 | Complete final report, figures, code documentation, and GitHub updates |

## 8. References

1. Boll, S. F. (1979). Suppression of acoustic noise in speech using spectral subtraction. IEEE Transactions on Acoustics, Speech, and Signal Processing, 27(2), 113-120.

2. Allen, J. B., and Rabiner, L. R. (1977). A unified approach to short-time Fourier analysis and synthesis. Proceedings of the IEEE, 65(11), 1558-1564.

3. Loizou, P. C. (2013). Speech Enhancement: Theory and Practice. CRC Press.

4. Rabiner, L. R., and Schafer, R. W. (2011). Theory and Applications of Digital Speech Processing. Pearson.
