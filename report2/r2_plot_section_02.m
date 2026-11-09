% Figure formatting for the report.
fig=figure('Position',[60 60 1050 700]);
tl=tiledlayout(3,1,'TileSpacing','loose','Padding','compact');
nexttile;
plot(timeFrames(validFrames), ...
    20*log10(percentileInfo.level(validFrames)+eps)); hold on;
pick=percentileInfo.selected & validFrames;
plot(timeFrames(pick),20*log10(percentileInfo.level(pick)+eps),'ro');
grid on; ylabel('Level (dB)');
legend('Noisy frame level','Lowest-energy frames','Location','northeastoutside');
title('Noise-estimation frame selection');
nexttile;
plot(timeFrames(validFrames), ...
    20*log10(vadInfo.level(validFrames)+eps)); hold on;
plot(timeFrames(validFrames), ...
    20*log10(vadInfo.noiseFloor(validFrames)+eps),'k--');
grid on; ylabel('Level (dB)'); legend('Noisy level','Tracked floor','Location','northeastoutside');
nexttile; stairs(timeFrames(validFrames), ...
    double(vadInfo.speech(validFrames)));
ylim([-0.1 1.1]); yticks([0 1]); yticklabels({'Noise','Speech'});
grid on; xlabel('Time (s)');
r2_save_figure(fig,outputFolder,'figure03_noise_estimation');
