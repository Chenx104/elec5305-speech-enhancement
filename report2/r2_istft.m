function x = r2_istft(Y, meta)
% Weighted overlap-add, followed by trimming to the original samples.
L = numel(meta.window); w = meta.window;
xp = zeros(meta.paddedLength,1); weights = xp;
assert(size(Y,2)==numel(meta.starts), 'STFT frame count mismatch.');
for m = 1:size(Y,2)
    spec = [Y(:,m); conj(Y(end-1:-1:2,m))];
    frame = real(ifft(spec,meta.nfft));
    idx = meta.starts(m):meta.starts(m)+L-1;
    xp(idx) = xp(idx) + frame(1:L).*w;
    weights(idx) = weights(idx) + w.^2;
end
keep = meta.padLeft+(1:meta.originalLength);
assert(all(weights(keep)>1e-8), 'Original samples lack reconstruction support.');
x = xp(keep)./weights(keep);
end
