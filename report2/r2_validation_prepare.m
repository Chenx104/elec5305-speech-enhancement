function [speech,noise,manifest]=r2_validation_prepare(folder,fs)
% Fixed-duration validation inputs; no artificial noise-only prefix is added.
data=fullfile(folder,'validation_data');
manifest=readtable(fullfile(data,'speech_manifest.csv'),'Delimiter',',','ReadVariableNames',true, ...
    'VariableNamingRule','preserve','TextType','string');
assert(height(manifest)==3 && numel(unique(manifest.SpeakerID))==3);
N=5*fs; speech=cell(3,1);
for k=1:3
    [s,sr]=audioread(fullfile(data,manifest.Filename(k)));
    manifest.SourceDuration_s(k)=size(s,1)/sr;
    s=mean(s,2);
    if sr~=fs, s=resample(s,fs,sr); end
    assert(numel(s)>=N,'Validation speech is shorter than 5 seconds.');
    s=s(1:N); s=s-mean(s); s=s/max(abs(s)); speech{k}=s;
end
[n,sr]=audioread(fullfile(folder,'car_idle_noise.mp3'));
n=mean(n,2); if sr~=fs, n=resample(n,fs,sr); end
[r,sr]=audioread(fullfile(data,'1-17367-A-10.wav'));
r=mean(r,2); if sr~=fs, r=resample(r,fs,sr); end
assert(numel(n)>=N && numel(r)>=N);
noise={n(1:N),r(1:N)};
for k=1:2
    v=noise{k}-mean(noise{k}); noise{k}=v/sqrt(mean(v.^2));
end
manifest.UsedDuration_s=repmat(5,3,1);
end
