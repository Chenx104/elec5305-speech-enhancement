function [out, detail] = r2_enhance_noisy(y, fs, cfg, method)
% Deployable processing interface: receives only the noisy recording.
[Y,meta] = r2_stft(y,cfg);
[P,info] = r2_noise_psd(Y,meta,fs,cfg,method);
G = r2_spectral_gain(Y,P,cfg);
out = r2_istft(G.*Y,meta);
detail = struct('Y',Y,'meta',meta,'Pnoise',P,'gain',G,'estimator',info);
end
