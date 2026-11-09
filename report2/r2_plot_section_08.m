% Figure formatting for the report.
fig=figure('Position',[60 60 1150 450]); tiledlayout(1,2, ...
    'TileSpacing','compact');
for ni=1:2
    nexttile; pick=alphaSweep.Noise==noiseNames(ni);
    xx=alphaSweep.NoiseReduction_dB(pick); yy=100-alphaSweep.SpeechRetained_pct(pick);
    plot(xx,yy,'-o','LineWidth',1.4); grid on;
    xlim([0 1.15*max(alphaSweep.NoiseReduction_dB)]);
    ylim([0 1.25*max(100-alphaSweep.SpeechRetained_pct)]);
    for ai=1:numel(xx)
        offset=0.35;
        if mod(ai,2)==0, offset=-0.55; end
        text(xx(ai),yy(ai)+offset, ...
            sprintf('%.1f',alphaValues(ai)), ...
            'FontSize',9,'HorizontalAlignment','center');
    end
    xlabel('Noise attenuation (dB)'); ylabel('Speech energy loss (%)');
    title(r2_label(noiseNames(ni)),'Interpreter','none');
end
r2_save_figure(fig,outputFolder,'figure11_alpha_tradeoff');

