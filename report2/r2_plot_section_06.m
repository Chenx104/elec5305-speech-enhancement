% Figure formatting for the report.
fig=figure('Position',[60 60 900 340]);
tiledlayout(1,2,'TileSpacing','loose','Padding','compact');
metricNames={'SNR_dB','SI_SDR_dB'};
metricLabels={'Output SNR (dB)','SI-SDR (dB)'};
methodLabels={'Noisy','Percentile','VAD','True PSD','Oracle'};
for k=1:2
    nexttile; barh(referenceTable.(metricNames{k})); grid on;
    yticks(1:height(referenceTable));
    if k==1, yticklabels(methodLabels); else, yticklabels({}); end
    set(gca,'YDir','reverse'); xlabel(metricLabels{k});
end
r2_save_figure(fig,outputFolder,'figure08_reference_comparison');
