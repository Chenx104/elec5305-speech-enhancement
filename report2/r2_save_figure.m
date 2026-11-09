function r2_save_figure(fig, outdir, name)
% Compact figures with consistent fonts for Live Script and PDF output.
keys={'figure02_input_signals','figure03_noise_estimation','figure04_gain', ...
    'figure05_waveforms','figure06_spectrograms','figure07_practical_multi_snr', ...
    'figure08_reference_comparison','figure09_including_oracle', ...
    'figure10_speech_noise_decomposition','figure11_alpha_tradeoff', ...
    'figure12_validation'};
captions={'Figure 2. Speech and car-idle inputs', ...
    'Figure 3. Noise-frame selection and VAD', ...
    'Figure 4. Percentile subtraction gain', ...
    'Figure 5. Main 5 dB waveforms', ...
    'Figure 6. Main 5 dB spectrograms', ...
    'Figure 7. SI-SDR across input SNRs', ...
    'Figure 8. Main 5 dB reference comparison', ...
    'Figure 9. Spectrograms with VAD and oracle', ...
    'Figure 10. Noise attenuation and speech energy', ...
    'Figure 11. Alpha sweep: attenuation and speech loss', ...
    'Figure 12. Additional validation'};
heights=[320 430 280 410 440 310 300 520 350 360 480];
idx=find(strcmp(name,keys),1);
set(fig,'Color','w','NumberTitle','off','Units','pixels');
if ~isempty(idx)
    set(fig,'Position',[60 60 820 heights(idx)],'Name',captions{idx});
end
axesList=findall(fig,'Type','axes');
for k=1:numel(axesList)
    ax=axesList(k);
    ax.Toolbar.Visible='off';
    ax.FontName='Arial'; ax.FontUnits='points'; ax.FontSize=10;
    ax.LabelFontSizeMultiplier=1; ax.TitleFontSizeMultiplier=1;
    ax.XLabel.FontSize=10; ax.YLabel.FontSize=10;
    ax.Title.FontSize=10; ax.Title.FontWeight='normal';
end
legends=findall(fig,'Type','legend');
for k=1:numel(legends)
    legends(k).FontSize=9;
end
colourbars=findall(fig,'Type','colorbar');
for k=1:numel(colourbars)
    colourbars(k).FontSize=9;
    colourbars(k).Label.FontSize=10;
end
layouts=findall(fig,'Type','tiledlayout');
for k=1:numel(layouts)
    layouts(k).XLabel.FontSize=10;
    layouts(k).YLabel.FontSize=10;
end
for k=1:numel(layouts)
    layouts(k).Title.String='';
end
drawnow;
exportgraphics(fig,fullfile(outdir,[name '.png']),'Resolution',180);
savefig(fig,fullfile(outdir,[name '.fig']));
end
