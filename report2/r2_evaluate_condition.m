function [T, bundle] = r2_evaluate_condition(x,d,fs,cfg)
% Clean/noise references are used only for evaluation and labelled references.
y=x+d; [X,meta]=r2_stft(x,cfg); D=r2_stft(d,cfg); Y=r2_stft(y,cfg);
trueMeanNoise=mean(abs(D(:,meta.fullFrames)).^2,2);
names={'Noisy','Percentile_SS','VAD_SS','TruePSD_SS_reference','Oracle_Wiener_reference'};
rows=cell(numel(names),1); bundle=struct;
for k=1:numel(names)
    name=names{k}; info=[]; psdError=NaN; selectedRatio=NaN;
    switch name
        case 'Noisy'
            G=ones(size(Y)); z=y;
        case {'Percentile_SS','VAD_SS'}
            if strcmp(name,'Percentile_SS'), method='percentile'; else, method='vad'; end
            [z,detail]=r2_enhance_noisy(y,fs,cfg,method);
            G=detail.gain; info=detail.estimator;
            % Compare mean estimated bin power with true mean noise bin power.
            pMean=mean(detail.Pnoise(:,meta.fullFrames),2);
            psdError=mean(abs(10*log10(max(pMean,realmin)./max(trueMeanNoise,realmin))));
            pick=info.selected & meta.fullFrames;
            if any(pick)
                selectedRatio=10*log10(max(sum(abs(X(:,pick)).^2,'all'),realmin)/ ...
                    max(sum(abs(D(:,pick)).^2,'all'),realmin));
            end
        case 'TruePSD_SS_reference'
            G=r2_spectral_gain(Y,trueMeanNoise,cfg); z=r2_istft(G.*Y,meta);
        case 'Oracle_Wiener_reference'
            raw=abs(X).^2./max(abs(X).^2+abs(D).^2,realmin);
            G=cfg.oracleFloor+(1-cfg.oracleFloor)*raw;
            z=r2_istft(G.*Y,meta);
    end
    % Freeze the gain estimated from y: never re-estimate it on x or d.
    sx=r2_istft(G.*X,meta); dn=r2_istft(G.*D,meta);
    result=r2_metrics(x,d,z,sx,dn,fs,cfg.computeSTOI);
    assert(result.DecompositionRelativeError<1e-10,'Frozen-gain decomposition failed.');
    result.Method=string(name); result.NoisePSDMeanAbsError_dB=psdError;
    result.SelectedFrameSpeechToNoise_dB=selectedRatio;
    rows{k}=struct2table(result);
    bundle.(name)=struct('out',z,'speech',sx,'noise',dn,'gain',G,'info',info);
end
T=vertcat(rows{:}); bundle.meta=meta; bundle.noisy=y;
end
