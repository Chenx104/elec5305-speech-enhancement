# STFT-Based Speech Enhancement

## Project Overview

This project investigates speech enhancement for noisy audio signals using short-time Fourier transform (STFT) based processing. Speech recordings are often affected by background noise, which reduces intelligibility and makes audio analysis more difficult. The aim of this project is to analyse noisy speech in the time-frequency domain and apply spectral subtraction to reduce noise while preserving the main speech components.

## Background and Motivation

Speech enhancement is an important topic in audio signal processing, hearing technology, telecommunications, and speech recognition. In real-world environments, speech can be corrupted by background sounds such as traffic, fans, room noise, or other speakers. Since speech is a non-stationary signal, a single Fourier transform is not enough to describe how its frequency content changes over time. STFT provides a practical way to analyse speech frame by frame using windowing, FFT, and overlap between frames.

This project is closely related to ELEC5305 topics including sampling, aliasing, DFT/FFT, filtering, audio features, spectrograms, STFT, inverse STFT, and overlap-add reconstruction.

## Proposed Method

The project will use MATLAB to process a clean speech signal and generate a noisy version by adding background noise. The noisy speech will be analysed using waveform plots, frequency spectra, and spectrograms. STFT will be applied by dividing the signal into overlapping windowed frames and computing the FFT of each frame.

A spectral subtraction method will then be used to estimate and reduce the noise component in the frequency domain. The enhanced speech will be reconstructed using inverse STFT and overlap-add. The final result will be compared with the original noisy signal.

## Course Concepts Used

- Sampling rate and normalized frequency
- Aliasing and Nyquist theorem
- DFT and FFT
- Digital filtering
- Windowing
- STFT and spectrogram analysis
- Inverse STFT
- Overlap-add reconstruction
- Audio features such as RMS energy, zero-crossing rate, and spectral centroid

## Expected Outcomes

The expected outcomes of this project include:

- Clean, noisy, and enhanced speech waveform plots
- Frequency spectrum comparison
- Spectrogram comparison before and after enhancement
- Basic speech quality evaluation using SNR improvement
- Audio feature comparison using RMS energy, zero-crossing rate, and spectral centroid
- MATLAB implementation of an STFT-based speech enhancement system

## Tools

- MATLAB
- GitHub
- GitHub Pages
- Audio signal samples in WAV format

## References

1. Boll, S. F. (1979). Suppression of acoustic noise in speech using spectral subtraction. IEEE Transactions on Acoustics, Speech, and Signal Processing.
2. Allen, J. B., and Rabiner, L. R. (1977). A unified approach to short-time Fourier analysis and synthesis. Proceedings of the IEEE.
3. Loizou, P. C. (2013). Speech Enhancement: Theory and Practice. CRC Press.
