function [S,perSpeaker,seedSummary,fig]=r2_validation_summary(T)
% Average white-noise seeds within each speaker before comparing speakers.
methods=["Percentile_SS","VAD_SS"]; noises=["CarIdle","Rain","WhiteGaussian"];
ids=unique(T.SpeakerID); snrs=[0 5 10]; metrics= ...
    {'SNR_dB','SI_Gain_dB','STOI_Change','SpeechLoss_pct','NoiseReduction_dB'};
rows={};
for ni=1:3
 for si=1:3
  for mi=1:2
   for sp=1:numel(ids)
    pick=T.Noise==noises(ni) & T.InputSNR_dB==snrs(si) & ...
        T.Method==methods(mi) & T.SpeakerID==ids(sp);
    A=T(pick,:);
    R=struct('Noise',noises(ni),'Input_dB',snrs(si),'Method',methods(mi), ...
        'SpeakerID',ids(sp),'SeedCount',height(A));
    for k=1:numel(metrics), R.(metrics{k})=mean(A.(metrics{k})); end
    rows{end+1}=struct2table(R); %#ok<AGROW>
   end
  end
 end
end
perSpeaker=vertcat(rows{:}); rows={};
for ni=1:3
 for si=1:3
  for mi=1:2
   p=perSpeaker.Noise==noises(ni) & perSpeaker.Input_dB==snrs(si) & ...
       perSpeaker.Method==methods(mi); A=perSpeaker(p,:);
   R=struct('Noise',noises(ni),'Input_dB',snrs(si),'Method',methods(mi), ...
       'Speakers',height(A),'SeedsPerSpeaker',A.SeedCount(1));
   for k=1:numel(metrics)
    v=A.(metrics{k}); R.([metrics{k} '_Mean'])=mean(v);
    R.([metrics{k} '_Min'])=min(v); R.([metrics{k} '_Max'])=max(v);
   end
   rows{end+1}=struct2table(R); %#ok<AGROW>
  end
 end
end
S=vertcat(rows{:}); rows={};
for seed=[5305 5306 5307]
 for si=1:3
  for mi=1:2
   p=T.Noise=="WhiteGaussian" & T.Seed==seed & ...
       T.InputSNR_dB==snrs(si) & T.Method==methods(mi);
   R=struct('Seed',seed,'Input_dB',snrs(si),'Method',methods(mi), ...
       'MeanSIGain_dB',mean(T.SI_Gain_dB(p)), ...
       'MeanSTOIChange',mean(T.STOI_Change(p)));
   rows{end+1}=struct2table(R); %#ok<AGROW>
  end
 end
end
seedSummary=vertcat(rows{:});
fig=figure('Position',[60 60 900 580]);
tl=tiledlayout(2,3,'TileSpacing','loose','Padding','compact');
fields={'SI_Gain_dB','STOI_Change'};
for row=1:2
 for ni=1:3
  nexttile; hold on;
  bounds=[]; handles=gobjects(1,2);
  for mi=1:2
   p=S.Noise==noises(ni) & S.Method==methods(mi); A=S(p,:);
   v=A.([fields{row} '_Mean']); lo=A.([fields{row} '_Min']); hi=A.([fields{row} '_Max']);
   bounds=[bounds;lo;hi];
   handles(mi)=errorbar(A.Input_dB,v,v-lo,hi-v,'-o','LineWidth',1.2);
  end
  yline(0,'k:'); grid on; xlabel('Input SNR (dB)');
  if row==1, ylabel('SI-SDR improvement (dB)'); else, ylabel('STOI change'); end
  title(r2_label(noises(ni)),'Interpreter','none');
  span=max(bounds)-min(bounds); pad=max(0.1*span,eps);
  ylim([min([bounds;0])-pad,max([bounds;0])+pad]);
  if row==1 && ni==1
      lg=legend(handles,r2_label(methods),'Interpreter','none', ...
          'Orientation','horizontal','AutoUpdate','off');
      lg.Layout.Tile='south';
  end
 end
end

end
