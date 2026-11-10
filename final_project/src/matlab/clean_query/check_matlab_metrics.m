function check_matlab_metrics(root)
addpath(fullfile(root,'matlab'));
a=load(fullfile(root,'metric_check.mat'));actual=zeros(size(a.expected));
for i=1:size(a.scores,2)
 m=p_verification_metrics(a.scores(:,i),a.genuine,a.threshold);
 actual(i,:)=100*[m.EER m.FAR m.FRR m.BER];
end
maxError=max(abs(actual-a.expected),[],'all');assert(maxError<1e-10);
fid=fopen(fullfile(root,'matlab_validation.json'),'w');fprintf(fid,'%s',jsonencode(struct( ...
 'OriginalMATLABMetricFunctionUsed',true,'Methods',size(actual,1), ...
 'MaximumPythonMATLABDifferencePercentagePoints',maxError,'Passed',true),PrettyPrint=true));fclose(fid);
fprintf('MATLAB_METRICS_VERIFIED maximum difference %.3g percentage points\n',maxError);
end
