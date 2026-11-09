function r2_print_diagnostics(p,v,valid,X,D,pairs)
% Reference-based checks, evaluated after enhancement.
infos={p,v}; names={'Percentile','VAD'};
for k=1:2
    chosen=infos{k}.selected & valid;
    sx=sum(abs(X(:,chosen)).^2,'all');
    dn=sum(abs(D(:,chosen)).^2,'all');
    fprintf('%s: %d/%d frames; selected X/D %.2f dB\n', ...
        names{k},sum(chosen),sum(valid),10*log10(sx/dn));
end
n=height(pairs);
fprintf('Percentile SI-SDR wins: %d/%d; STOI wins: %d/%d\n', ...
    sum(pairs.SIAdvantage_dB>0),n,sum(pairs.STOIAdvantage>0),n);
fprintf('Different method rankings: %d/%d\n', ...
    sum(pairs.RankingDisagrees),n);
end
