function T=r2_validation_run(speech,noise,manifest,fs,cfg)
% Environmental clips are fixed; white-noise seeds are repeated within speaker.
noiseNames=["CarIdle","Rain","WhiteGaussian"];
seeds=[5305 5306 5307]; snrs=[0 5 10]; rows={};
savedRng=rng; restoreRng=onCleanup(@()rng(savedRng)); %#ok<NASGU>
for sp=1:numel(speech)
    x=speech{sp}; N=numel(x);
    for ni=1:3
        if ni==3, repeats=1:numel(seeds); else, repeats=1; end
        for rep=repeats
            if ni==3
                seed=seeds(rep); rng(seed,'twister');
                n=randn(N,1); n=n-mean(n); n=n/sqrt(mean(n.^2));
            else
                seed=0; n=noise{ni};
            end
            for si=1:numel(snrs)
                d=n*sqrt(mean(x.^2)/10^(snrs(si)/10));
                [A,~]=r2_evaluate_condition(x,d,fs,cfg);
                keep=ismember(A.Method,["Noisy","Percentile_SS","VAD_SS"]);
                A=A(keep,:);
                measured=10*log10(sum(x.^2)/sum(d.^2));
                assert(abs(measured-snrs(si))<1e-10);
                A.SpeakerID=repmat(manifest.SpeakerID(sp),height(A),1);
                A.UtteranceID=repmat(manifest.UtteranceID(sp),height(A),1);
                A.Noise=repmat(noiseNames(ni),height(A),1);
                A.InputSNR_dB=repmat(snrs(si),height(A),1);
                A.Seed=repmat(seed,height(A),1);
                A.SI_Gain_dB=A.SI_SDR_dB-A.SI_SDR_dB(A.Method=="Noisy");
                A.STOI_Change=A.STOI-A.STOI(A.Method=="Noisy");
                A.SpeechLoss_pct=100-A.SpeechRetained_pct;
                rows{end+1}=A; %#ok<AGROW>
            end
        end
    end
end
T=vertcat(rows{:}); assert(height(T)==135);
assert(max(T.DecompositionRelativeError)<1e-10);
end
