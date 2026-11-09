function G = r2_spectral_gain(Y, Pnoise, cfg)
% Identical power-subtraction rule for every PSD-estimator comparison.
Py = abs(Y).^2;
Pclean = max(Py-cfg.alpha*Pnoise,cfg.beta*Py);
G = sqrt(Pclean./max(Py,realmin));
% A zero-energy bin may use any gain; the floor keeps the rule continuous.
G(Py==0) = sqrt(cfg.beta);
assert(all(isfinite(G(:))) && all(G(:)>=0) && all(G(:)<=1+1e-12));
end
