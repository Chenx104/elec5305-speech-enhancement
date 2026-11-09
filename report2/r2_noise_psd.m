function [P, info] = r2_noise_psd(Y, meta, fs, cfg, method)
% Only noisy STFT data enter this estimator; no clean/noise references.
power = abs(Y).^2; valid = find(meta.fullFrames);
% Unweighted spectral frame level for the simplified VAD.
level = sqrt(mean(power,1));
selected = false(1,size(Y,2)); speech = false(1,size(Y,2));
floorTrack = nan(1,size(Y,2));
switch method
    case 'percentile'
        threshold = prctile(level(valid),cfg.noisePercentile);
        selected(valid) = level(valid)<=threshold;
        p = mean(power(:,selected),2);
        P = repmat(p,1,size(Y,2));
    case 'vad'
        % Assumption: the first cfg.initNoiseSeconds of complete frames are
        % noise-dominated. Test this assumption using references only later.
        dt = cfg.hopSize/fs;
        assert(dt<cfg.floorFallSeconds,'Tutorial 6 requires hop time < 0.04 s.');
        nInit = min(numel(valid),max(1,ceil(cfg.initNoiseSeconds/dt)));
        init = valid(1:nInit);
        p = mean(power(:,init),2);
        noiseFloor = max(median(level(init)),sqrt(eps));
        state = false; smooth = exp(-dt/cfg.psdTimeConstant);
        P = zeros(size(power));
        for m = 1:size(Y,2)
            if meta.fullFrames(m)
                if m <= init(end)
                    state = false;
                elseif level(m)>cfg.vadSpeechRatio*noiseFloor
                    state = true;
                elseif level(m)<cfg.vadNoiseRatio*noiseFloor
                    state = false;
                end % Between thresholds, retain the previous state.
                speech(m) = state; selected(m) = ~state;
                if m>init(end) && ~state
                    p = smooth*p + (1-smooth)*power(:,m);
                end
                if level(m)>noiseFloor
                    tau = cfg.floorRiseSeconds;
                else
                    tau = cfg.floorFallSeconds;
                end
                % Tutorial 6 Q5: slow rise dt/10; fast fall dt/0.04.
                noiseFloor = max(noiseFloor + ...
                    (level(m)-noiseFloor)*(dt/tau),sqrt(eps));
            end
            P(:,m) = p; floorTrack(m) = noiseFloor;
        end
    otherwise
        error('Unknown estimator: %s',method);
end
info = struct('selected',selected,'speech',speech, ...
    'level',level,'noiseFloor',floorTrack);
end
