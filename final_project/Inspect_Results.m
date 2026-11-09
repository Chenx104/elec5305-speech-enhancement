function T=Inspect_Results()
% Read stored formal results only. Does not invoke preprocessing or models.
root=fileparts(mfilename('fullpath'));
T=readtable(fullfile(root,'results','tables','test','test_summary.csv'),'TextType','string');
T=T(T.ReferenceSet=="enrollment_primary",:);
keep=["Noisy","SS_a1p5","Tracking_SS","DeepFilterNet"];
[ok,idx]=ismember(keep,T.Method);assert(all(ok));T=T(idx,:);
disp(T(:,{'Method','TargetSI_SDRGain_dB','TargetSTOIChange','ExternalEER_pct','CommonThresholdBER_pct'}));
figure('Color','w','Name','Formal external verification');bar(categorical(T.Method,T.Method),T.ExternalEER_pct);
ylabel('External-verification EER (%)');title('Stored full test results: 1080 mixtures');grid on;
end
