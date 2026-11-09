function [diagnostic, paired]=r2_metric_agreement(T)
% Reference-based diagnostics; these values never alter enhancement gains.
methods=["Percentile_SS","VAD_SS"];
noises=["CarIdle","Rain","WhiteGaussian"];
ids=unique(T.SpeakerID); rows={};
for ni=1:numel(noises)
    for mi=1:numel(methods)
        ratio=zeros(numel(ids),1); loss=ratio;
        for sp=1:numel(ids)
            p=T.Noise==noises(ni) & T.Method==methods(mi) & ...
                T.SpeakerID==ids(sp) & T.InputSNR_dB==5;
            ratio(sp)=mean(T.SelectedFrameSpeechToNoise_dB(p));
            loss(sp)=mean(T.SpeechLoss_pct(p));
        end
        rows{end+1}=table(noises(ni),methods(mi), ...
            mean(ratio),mean(loss),'VariableNames', ...
            {'Noise','Method','SelectedRatio_dB','SpeechLoss_pct'});
    end
end
diagnostic=vertcat(rows{:});
keys={'SpeakerID','Noise','InputSNR_dB','Seed'};
A=sortrows(T(T.Method==methods(1),:),keys);
B=sortrows(T(T.Method==methods(2),:),keys);
assert(isequal(A(:,keys),B(:,keys)),'Mixture pairing failed.');
paired=A(:,keys);
paired.SIAdvantage_dB=A.SI_Gain_dB-B.SI_Gain_dB;
paired.STOIAdvantage=A.STOI_Change-B.STOI_Change;
paired.RankingDisagrees= ...
    paired.SIAdvantage_dB.*paired.STOIAdvantage<0;
assert(height(paired)==45,'Unexpected mixture count.');
end
