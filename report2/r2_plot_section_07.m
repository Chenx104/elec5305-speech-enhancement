% Figure formatting for the report.
fig=figure('Position',[60 60 1250 500]); tiledlayout(1,2, ...
    'TileSpacing','compact');
labels=["Car / Percentile","Car / VAD","White / Percentile","White / VAD"];
nexttile; bar(preservationTable.NoiseReduction_dB); ylabel('Noise attenuation (dB)');
grid on; xticks(1:height(preservationTable)); xticklabels(labels); xtickangle(25);
set(gca,'TickLabelInterpreter','none');
nexttile; bar(preservationTable.SpeechRetained_pct); ylabel('Speech retained (%)');
grid on; xticks(1:height(preservationTable)); xticklabels(labels); xtickangle(25);
set(gca,'TickLabelInterpreter','none');
r2_save_figure(fig,outputFolder,'figure10_speech_noise_decomposition');
