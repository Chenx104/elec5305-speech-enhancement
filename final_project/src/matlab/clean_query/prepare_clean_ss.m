function prepare_clean_ss(root)
% Exact original MATLAB DSP helpers, applied to unique pre-mixture clean crops.
addpath(fullfile(root,'matlab'));
c=jsondecode(fileread(fullfile(root,'test_config.json')));cfg=c.cfg;assert(cfg.alpha==1.5 && cfg.beta==.02);
M=readtable(fullfile(root,'clean_manifest.csv'),'Delimiter',',','ReadVariableNames',true,'TextType','string','VariableNamingRule','preserve');
C=readtable(fullfile(root,'dsp','base_clip_index.csv'),'Delimiter',',','ReadVariableNames',true,'TextType','string','VariableNamingRule','preserve');
Q=M(M.RecordingRole=="test",:);assert(height(Q)==90);
extra=C([],:);diag=struct([]);
for i=1:height(Q)
 r=Q(i,:);[x,sr]=audioread(r.CleanPath);assert(sr==16000 && numel(x)==80000);
 [Y,meta]=p_stft(x,cfg);[PSD,info]=p_noise_psd(Y,meta,sr,cfg,'percentile');
 G=p_spectral_gain(Y,PSD,cfg);z=p_istft(G.*Y,meta);
 gain=c.export_headroom/max(1,max([abs(x);abs(z)]));
 assert(abs(gain-double(r.ExportGain))<1e-12,'Clean/SS shared gain differs from existing clean export.');
 id="cleanprobe_"+r.UtteranceID+"_SS_a1p5";dest=fullfile(root,'dsp','audio16k',id+".wav");
 audiowrite(dest,gain*z,sr,'BitsPerSample',24);
 row=C(C.UtteranceID==r.UtteranceID,:);assert(height(row)==1);
 row.ClipID=id;row.Method="SS_a1p5";row.Path=string(dest);extra=[extra;row]; %#ok<AGROW>
 [cleanExport,~]=audioread(r.ECAPAInputPath);assert(max(abs(cleanExport-gain*x))<=2^-23+eps);
 residual=p_istft(Y,meta)-x;
 energyRatio=sum(z.^2)/sum(x.^2);
 diag=[diag;struct('UtteranceID',r.UtteranceID,'ParticipantRole',r.ParticipantRole, ...
  'ExportGain',gain,'SelectedFrames',nnz(info.selected),'CleanInputPeak',max(abs(x)), ...
  'OutputEnergyRatio',energyRatio,'MeanPowerGain',mean(G(:).^2), ...
  'STFTRelativeError',norm(residual)/norm(x))]; %#ok<AGROW>
end
writetable([C;extra],fullfile(root,'dsp','clip_index.csv'));
writetable(struct2table(diag),fullfile(root,'dsp','clean_ss_diagnostics.csv'));
fprintf('CLEAN_SS_COMPLETE: %d unique queries, original alpha %.1f and beta %.2f\n',height(Q),cfg.alpha,cfg.beta);
end
