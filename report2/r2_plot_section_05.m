% Figure formatting for the report.
methods=["Noisy","Percentile_SS","VAD_SS"];
fig=figure('Position',[60 60 1150 450]); tl=tiledlayout(1,2, ...
    'TileSpacing','loose','Padding','compact');
for ni=1:2
    nexttile; hold on;
    for mi=1:numel(methods)
        pick=results.Noise==noiseNames(ni) & results.Method==methods(mi);
        plot(results.TargetSNR_dB(pick),results.SI_SDR_dB(pick),'-o', ...
    'LineWidth',1.4);
    end
    grid on; xlabel('Input SNR (dB)'); ylabel('SI-SDR (dB)');
    title(r2_label(noiseNames(ni)),'Interpreter','none');
    if ni==1
        lg=legend({'Noisy','Percentile','VAD'},'Orientation','horizontal');
        lg.Layout.Tile='south';
    end
end
r2_save_figure(fig,outputFolder,'figure07_practical_multi_snr');
