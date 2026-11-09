% Figure formatting for the report.
fig=figure('Position',[60 60 1000 600]);
tiledlayout(2,1,'TileSpacing','compact');
nexttile; plot(t,x); grid on; xlim([0 N/fs]);
xlabel('Time (s)'); ylabel('Amplitude'); title('Clean speech');
nexttile; plot(t,n); grid on; xlim([0 N/fs]);
xlabel('Time (s)'); ylabel('Amplitude'); title('Car-idle source, unit RMS');
r2_save_figure(fig,outputFolder,'figure02_input_signals');
if PLAY_AUDIO
    sourceGain=0.95/max([max(abs(x)),max(abs(n))]);
    disp('Clean speech'); sound(sourceGain*x,fs); pause(N/fs+0.5);
    disp('Car-idle noise'); sound(sourceGain*n,fs); pause(N/fs+0.5);
end
