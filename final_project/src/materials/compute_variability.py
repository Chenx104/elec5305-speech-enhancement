"""Noise-only variability audit; no enhancement or speaker models are imported."""
import csv,json,hashlib
from pathlib import Path
import numpy as np,soundfile as sf
from scipy.signal import resample_poly
r=Path(__file__).resolve().parent;inventory=json.loads((r/'channel01_inventory.json').read_text());edges=np.array([0,250,500,1000,2000,4000,8000]);L=512;H=256;fs=16000;win=np.hanning(L+1)[:-1];freq=np.fft.rfftfreq(L,1/fs);weights=np.full(L//2+1,2.);weights[[0,-1]]=1;rows=[];traces=r/'energy_traces';traces.mkdir(exist_ok=True);analysis=r/'analysis16k';analysis.mkdir(exist_ok=True)
for rec in inventory:
 env=rec['Environment'];x,sr=sf.read(rec['Path'],dtype='float64');assert np.isfinite(x).all() and x.ndim==1
 if sr!=fs:x=resample_poly(x,1,3);assert sr==48000
 # Save the actual analysis waveform separately from the original channel.
 dest=analysis/(env+'_ch01_16k.wav');sf.write(dest,x,fs,subtype='FLOAT');x,_=sf.read(dest,dtype='float64');x=x-x.mean();rms=np.sqrt(np.mean(x*x));assert rms>1e-12;x=x/rms
 frames=np.lib.stride_tricks.sliding_window_view(x,L)[::H];power=[]
 for i in range(0,len(frames),2048):
  z=np.fft.rfft(frames[i:i+2048]*win,axis=1);p=abs(z)**2*weights/(L*np.sum(win*win));b=[]
  for k in range(6):
   sel=(freq>=edges[k]) & (freq<edges[k+1] if k<5 else freq<=edges[k+1]);b.append(p[:,sel].sum(axis=1))
  power.append(np.column_stack(b))
 power=np.vstack(power);med=np.median(power,axis=0);valid=med>=med.max()*1e-6;assert valid.sum()>=3;db=10*np.log10(np.maximum(power,1e-12));q10,q90=np.quantile(db,[.1,.9],axis=0,method='linear');spread=q90-q10;V=float(np.median(spread[valid]));row={'Environment':env,'Duration_s':len(x)/fs,'Full5sSlots':len(x)//(5*fs),'V_dB':V,'ValidBands':int(valid.sum()),'NativeSampleRate':sr,'InputSHA256':rec['SourceSHA256'],'AnalysisSHA256':hashlib.sha256(dest.read_bytes()).hexdigest(),'AnalysisPath':str(dest.resolve())}
 for k in range(6):row[f'Band{int(edges[k])}_{int(edges[k+1])}_Spread_dB']=float(spread[k]);row[f'Band{int(edges[k])}_{int(edges[k+1])}_Valid']=bool(valid[k])
 rows.append(row)
 trace=np.column_stack(((np.arange(len(frames))*H+(L-1)/2)/fs,db));np.savetxt(traces/(env+'.csv'),trace,delimiter=',',header='Time_s,'+','.join(f'Band{int(edges[k])}_{int(edges[k+1])}_dB' for k in range(6)),comments='');print(env,'V=',round(V,4),'dB',flush=True)
rows.sort(key=lambda z:(z['V_dB'],z['Environment']))
with (r/'variability_all_sources.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'environment_count':len(rows),'fixed_channel':'ch01','definition':'Median over retained bands of full-recording frame-band-energy P90-P10 in dB','window_samples':L,'hop_samples':H,'fft_samples':L,'band_edges_hz':edges.tolist(),'candidate_low_3dB_count':sum(x['V_dB']<=3 for x in rows),'candidate_high_6dB_count':sum(x['V_dB']>=6 for x in rows),'sorted_sources':[{k:x[k] for k in ['Environment','V_dB','Duration_s','Full5sSlots']} for x in rows]};(r/'variability_summary.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
