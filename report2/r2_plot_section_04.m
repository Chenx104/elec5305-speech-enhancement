% Figure formatting for the report.
fig=figure('Position',[60 60 1050 700]); tiledlayout(3,1, ...
    'TileSpacing','compact');
waveNames={'Clean speech','Noisy speech','Percentile enhanced speech'};
waveSignals={x,yMain,enhanced};
waveLimit=max(cellfun(@(v)max(abs(v)),waveSignals));
for k=1:3
    nexttile; plot(t,waveSignals{k}); ylim([-waveLimit waveLimit]);
    grid on; xlim([0 N/fs]); xlabel('Time (s)'); ylabel('Amplitude'); title(waveNames{k});
end
r2_save_figure(fig,outputFolder,'figure05_waveforms');
