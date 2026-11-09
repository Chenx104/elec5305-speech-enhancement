% Figure formatting for the report.
fig=figure('Position',[60 60 1000 430]);
imagesc(timeFrames(validFrames),freqAxis/1000,20*log10(gain(:, ...
    validFrames)+eps));
axis xy; xlabel('Time (s)'); ylabel('Frequency (kHz)');
cb=colorbar; cb.Label.String='Amplitude gain (dB)';
title('Car-idle, input SNR = 5 dB');
r2_save_figure(fig,outputFolder,'figure04_gain');
