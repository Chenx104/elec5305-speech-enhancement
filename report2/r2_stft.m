function [Y, meta] = r2_stft(x, cfg)
% Padded, one-sided STFT. Estimators must exclude synthetic boundary frames.
x = x(:); L = cfg.winLength; H = cfg.hopSize; F = cfg.nfft;
assert(F >= L && mod(F,2)==0, 'Use an even FFT length >= window length.');
w = hann(L, 'periodic');
xp = [zeros(L,1); x; zeros(L + mod(-length(x),H),1)];
starts = 1:H:(length(xp)-L+1);
Y = zeros(F/2+1, numel(starts));
for m = 1:numel(starts)
    idx = starts(m):starts(m)+L-1;
    spec = fft(xp(idx).*w, F);
    Y(:,m) = spec(1:F/2+1);
end
meta = struct('window',w,'starts',starts,'paddedLength',length(xp), ...
    'originalLength',length(x),'padLeft',L,'nfft',F);
meta.fullFrames = starts >= L+1 & starts+L-1 <= L+length(x);
assert(any(meta.fullFrames), 'Recording must contain at least one full frame.');
end
