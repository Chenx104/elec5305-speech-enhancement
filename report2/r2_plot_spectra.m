function fig=r2_plot_spectra(signals,labels,fs,cfg,figureTitle,nColumns)
% One STFT and colour scale, with shared axis labels across all panels.
[~,meta]=r2_stft(signals{1},cfg); valid=meta.fullFrames;
t=(meta.starts(valid)-1-meta.padLeft+cfg.winLength/2)/fs;
f=(0:cfg.nfft/2)*fs/cfg.nfft/1000;
levels=cell(size(signals));
for k=1:numel(signals)
    S=r2_stft(signals{k},cfg); levels{k}=20*log10(abs(S(:,valid))+1e-12);
end
top=max(levels{1},[],'all');
nRows=ceil(numel(signals)/nColumns);
fig=figure('Position',[60 60 900 max(450,220*nRows)]);
tl=tiledlayout(nRows,nColumns,'TileSpacing','loose','Padding','compact');
for k=1:numel(signals)
    ax=nexttile; imagesc(t,f,levels{k}); axis xy; clim(ax,[top-80 top]);
    title(labels{k},'Interpreter','none');
end
xlabel(tl,'Time (s)'); ylabel(tl,'Frequency (kHz)');
cb=colorbar; cb.Layout.Tile='east';
cb.Label.String='STFT magnitude (dB, shared scale)';
title(tl,figureTitle);
end
