function label=r2_label(label)
% Reader-facing labels; stored result identifiers remain unchanged.
label=string(label);
keys=["Percentile_SS","VAD_SS","CarIdle","WhiteGaussian", ...
    "TruePSD_SS_reference","Oracle_Wiener_reference"];
values=["Percentile","VAD","Car idle","White noise", ...
    "True PSD","Oracle"];
for k=1:numel(keys), label=replace(label,keys(k),values(k)); end
end
