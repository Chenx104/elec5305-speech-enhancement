function fig=r2_plot_agreement(paired)
noises=["CarIdle","Rain","WhiteGaussian"];
fig=figure('Position',[60 60 820 350],'Color','w');
hold on;
for ni=1:numel(noises)
    p=paired.Noise==noises(ni);
    scatter(paired.SIAdvantage_dB(p),paired.STOIAdvantage(p), ...
        36,'filled','DisplayName',r2_label(noises(ni)));
end
xline(0,'k:','HandleVisibility','off');
yline(0,'k:','HandleVisibility','off');
xlabel('SI-SDR advantage: Percentile minus VAD (dB)');
ylabel('STOI advantage: Percentile minus VAD');
legend('Location','best'); grid on;
end
