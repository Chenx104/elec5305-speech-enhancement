"""Run the fixed official DeepFilterNet model once for each noisy mixture."""
from pathlib import Path
import csv,json,hashlib,subprocess,time,sys
import numpy as np,soundfile as sf
from scipy.signal import resample_poly,correlate,correlation_lags
R=Path(sys.argv[1]).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def writecsv(path,rows):
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 conf=json.loads((R/'test_config.json').read_text());assert conf['deepfilternet_extra_input_gain']==1
 rows=list(csv.DictReader((R/'dsp/clip_index.csv').open()));noisy=[r for r in rows if r['Method']=='Noisy'];assert len(noisy)==conf['expected_mixtures']
 out=R/'external';out.mkdir();staged=out/'input48k';raw=out/'raw48k';aligned=out/'audio16k'
 for p in [staged,raw,aligned]:p.mkdir()
 binary=R/'tools/deep-filter-0.5.6-aarch64-apple-darwin';model=R/'tools/DeepFilterNet3_onnx.tar.gz';pad=4800;delay=1440;calls=0;t=time.perf_counter()
 def infer(p,d,comp=True):
  nonlocal calls
  d.mkdir(exist_ok=True);args=[str(binary),'-m',str(model)]+(['-D'] if comp else [])+['-o',str(d),str(p)]
  q=subprocess.run(args,capture_output=True,text=True);calls+=1
  if q.returncode:raise RuntimeError(q.stdout+q.stderr)
  return d/p.name
 reference=next(r for r in rows if r['RecordingRole']=='enrollment_primary');x,sr=sf.read(reference['Path']);assert sr==16000;probe=resample_poly(x,3,1);p=staged/'alignment_probe.wav';sf.write(p,np.pad(probe,(0,pad)),48000,subtype='FLOAT')
 comp=infer(p,raw);u=infer(p,out/'uncompensated',False);y,_=sf.read(comp);v,_=sf.read(u);assert np.array_equal(y,v[delay:]);lag=int(correlation_lags(len(probe),len(probe))[np.argmax(correlate(y[:len(probe)],probe,method='fft'))]);assert abs(lag)<=1
 additions=[];provenance=[]
 for i,r in enumerate(noisy):
  x,sr=sf.read(r['Path'],dtype='float32');assert sr==16000 and len(x)==80000
  x48=resample_poly(x,3,1);p=staged/(r['ConditionID']+'.wav');sf.write(p,np.pad(x48,(0,pad)),48000,subtype='FLOAT');dest=infer(p,raw);y,sr=sf.read(dest,dtype='float32');assert sr==48000 and len(y)>=len(x48) and np.isfinite(y).all();peak=float(max(abs(y)));assert peak<.999
  pcm=staged/(r['ConditionID']+'_pcm16_control.wav');sf.write(pcm,x48,48000,subtype='PCM_16');q,_=sf.read(pcm,dtype='float32')
  variants={'DeepFilterNet':resample_poly(y[:len(x48)],1,3),'Resample_only':resample_poly(x48,1,3),'Adapter':resample_poly(q,1,3)};new=[];outputs={str(dest):sha(dest)}
  for method,z in variants.items():
   assert len(z)==80000 and np.isfinite(z).all();path=aligned/(r['ConditionID']+'_'+method+'.wav');sf.write(path,z,16000,subtype='FLOAT');outputs[str(path)]=sha(path);new.append({**r,'ClipID':r['ConditionID']+'_'+method,'Method':method,'Path':str(path.resolve())})
  pr={'ConditionID':r['ConditionID'],'NoisySHA256':sha(r['Path']),'Input48kSHA256':sha(p),'DeepFilterOutputSHA256':sha(aligned/(r['ConditionID']+'_DeepFilterNet.wav')),'RawPCM16Peak':peak}
  additions+=new;provenance.append(pr)
  if (i+1)%24==0 or i+1==len(noisy):print(f'DeepFilterNet {i+1}/{len(noisy)}',flush=True)
 writecsv(out/'complete_clip_index.csv',rows+additions)
 atomic(out/'deepfilter_audit.json',{'release':'v0.5.6','extra_input_gain':1,'model_delay_samples48k':delay,'right_padding_samples48k':pad,'alignment_lag_samples':lag,'inference_calls':calls,'elapsed_seconds':time.perf_counter()-t,'clips':provenance,'output_encoding':'official CLI PCM16; aligned signals FLOAT'})
 print('DEEPFILTERNET_COMPLETE',flush=True)
if __name__=='__main__':main()
