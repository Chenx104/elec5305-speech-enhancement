# Clean-Speech Verification Analysis

## Purpose

This analysis evaluates speaker verification on clean speech and examines the effect of applying enhancement to recordings without added noise. It uses the same ECAPA-TDNN verifier, enrollment references and scoring procedure as the noisy-speech experiments.

The analysis appears in **Section 25** of [`final_project.mlx`](../final_project.mlx); Section 26 presents the overall findings.

## Experimental protocol

The evaluation uses **90 distinct five-second test queries**: 60 utterances from the 20 enrolled speakers and 30 utterances from 10 external speakers. Inputs retain the original 16 kHz crops and preprocessing used before noise mixing. Each condition produces **60 genuine** and **600 external-impostor** verification trials.

Five input conditions are evaluated:

1. Clean speech without enhancement.
2. Clean speech processed by default MATLAB spectral subtraction (α = 1.5; β = 0.02).
3. Clean speech processed by DeepFilterNet3.
4. Resampling-only interface control.
5. PCM16 interface control.

Spectral subtraction estimates its noise spectrum directly from each clean recording. DeepFilterNet3 uses the same model and processing interface as in the noisy-speech experiment. Verification uses the original separate clean enrollment recordings and the fixed SpeechBrain ECAPA model. The common decision threshold is **0.270078811669524**, selected from the noisy-speech development data.

## Verification results

| Input condition | EER (%) | FAR (%) | FRR (%) | BER (%) | False accepts / 600 |
|---|---:|---:|---:|---:|---:|
| Clean | 0.000 | 2.500 | 0.000 | 1.250 | 15 |
| Clean + spectral subtraction | 0.167 | 4.000 | 0.000 | 2.000 | 24 |
| Clean + DeepFilterNet3 | 0.000 | 3.000 | 0.000 | 1.500 | 18 |
| Resampling-only control | 0.000 | 2.833 | 0.000 | 1.417 | 17 |
| PCM16 control | 0.000 | 2.833 | 0.000 | 1.417 | 17 |

EER is estimated across score thresholds; FAR, FRR and BER use the fixed development threshold. Here, BER = (FAR + FRR) / 2. No genuine trials are rejected at that operating threshold.

In the 600 external-impostor trials, default spectral subtraction produces nine more false accepts than Clean, and DeepFilterNet3 produces three more. These are small point-estimate differences without separate confidence intervals. The clean EER is 0% for both Clean and DeepFilterNet3, while the spectral-subtraction EER is 0.167%. The limited trial set warrants care when interpreting differences near zero EER; a single genuine-trial count corresponds to 1.667 percentage points of FRR, and a single impostor-trial count to approximately 0.167 percentage points of FAR. Interpolated EER is not constrained to those individual counting steps.

By comparison, noisy-speech verification produces EERs of **7.083%** for Noisy, **8.764%** for default spectral subtraction and **9.028%** for DeepFilterNet3. The clean results establish the low-error reference against which the larger noisy-condition error rates can be understood. The clean and noisy experiments use different numbers of trials and condition weightings, so their EER values are reported separately.

## Results and reproduction

- [Summary metrics](../results/tables/clean_query/clean_query_summary.csv)
- [Per-trial scores and decisions](../results/tables/clean_query/clean_query_trials.csv)
- [Paired decision changes](../results/tables/clean_query/paired_decision_changes.csv)
- [MATLAB metric-check data](../results/tables/clean_query/metric_check.mat)
- [Score distribution figure](../results/figures/clean_score_distributions.pdf)
- [Experiment audit records](../results/audits/clean_query/)
- [Python analysis scripts](../src/scripts/clean_query/)
- [MATLAB reproduction helpers](../src/matlab/clean_query/)

For a quick inspection, open `final_project.mlx` and view Section 25. With a clear MATLAB workspace, Section 25 reads the recorded clean-query results and checks their metrics without rerunning neural inference. A complete **Run All** generates fresh clean-query results for the current main experiment run after processing the development and noisy-test data. Reproduction requirements are described in [Data and Models](DATA_AND_MODELS.md).
