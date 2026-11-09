function result = r2_metrics(x, d, z, sx, dn, fs, computeSTOI)
% All measures use the entire padded-then-trimmed signal, before export gain.
x=x(:); d=d(:); z=z(:); sx=sx(:); dn=dn(:);
ratioDB = @(a,b) 10*log10(max(sum(a.^2),realmin)/max(sum(b.^2),realmin));
result.SNR_dB = ratioDB(x,z-x); % No least-squares output rescaling.
xc=x-mean(x); zc=z-mean(z);
a=(xc'*zc)/max(xc'*xc,realmin); target=a*xc;
result.SI_SDR_dB=ratioDB(target,zc-target); % Explicit zero-mean convention.
result.NoiseReduction_dB=ratioDB(d,dn);
result.SpeechRetained_pct=100*sum(sx.^2)/max(sum(x.^2),realmin);
result.SpeechDistortionSNR_dB=ratioDB(x,sx-x);
result.DecompositionRelativeError=norm(z-(sx+dn))/max(norm(z),realmin);
result.STOI=NaN;
if computeSTOI
    result.STOI=stoi(z,x,fs);
end
end
