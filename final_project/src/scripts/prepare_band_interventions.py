"""Apply the frozen band perturbation implementation to all 60 target test utterances."""
from pathlib import Path
import csv,json,hashlib,time
import numpy as np,soundfile as sf
from band_intervention import perturbations,BANDS
import sys
R=Path(sys.argv[1]).resolve()
if __name__=='__main__':
 out=R/'band_intervention';out.mkdir(exist_ok=True);audio=out/'audio16k';audio.mkdir(exist_ok=True)
 rows=[r for r in csv.DictReader((R/'inputs/clean_index.csv').open()) if r['RecordingRole']=='test' and r['ParticipantRole']=='target'];assert len(rows)>0
 records=[];max_energy_err=0;t=time.time()
 for i,r in enumerate(rows):
  x,sr=sf.read(r['CleanPath']);assert sr==16000;energy=float(x@x);variants=[('clean',0.,-1,0.,x)]
  for level in [3,6,12]:
   obj=perturbations(x,level);expected=obj['energy_ratio'];actual=[float(z@z)/energy for z in obj['energy_matched']];max_energy_err=max(max_energy_err,max(abs(a-expected) for a in actual))
   for bi in range(3):
    variants += [('fixed',level,bi,level,obj['fixed'][bi]),('fixed_level_control',level,bi,0.,obj['fixed_whole_level_controls'][bi]),('matched',level,bi,obj['matched_attenuation_db'][bi],obj['energy_matched'][bi])]
   variants += [('matched_level_control',level,-1,0.,obj['whole_level_control'])]
  assert len(variants)==31;gain=.5/max(1.,max(float(np.max(abs(z))) for *_,z in variants))
  for kind,level,bi,eff,z in variants:
   cid=f"band_{r['UtteranceID']}_{kind}_{int(level)}_{bi}";p=audio/(cid+'.wav');sf.write(p,z*gain,16000,subtype='PCM_24');back,_=sf.read(p)
   records.append({'ClipID':cid,'SpeakerID':r['SpeakerID'],'UtteranceID':r['UtteranceID'],'Kind':kind,'Level_dB':level,'BandIndex':bi,'BandLow_Hz':BANDS[bi][0] if bi>=0 else -1,'BandHigh_Hz':BANDS[bi][1] if bi>=0 else -1,'EffectiveAttenuation_dB':eff,'EnergyRatio':float(z@z)/energy,'ExportedEnergyRatio':float((back/gain)@(back/gain))/energy,'ExportGain':gain,'Path':str(p.resolve()),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest()})
  if (i+1)%10==0:print(f'Band interventions {i+1}/60; {time.time()-t:.1f}s',flush=True)
 with (out/'clip_index.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 (out/'preparation_audit.json').write_text(json.dumps({'target_test_utterances':len(rows),'clips':len(records),'frozen_algorithm_SHA256':hashlib.sha256((Path(__file__).parent/'band_intervention.py').read_bytes()).hexdigest(),'maximum_before_export_energy_mismatch':max_energy_err,'all_variants_same_gain_within_utterance':True,'parameters_changed':False},indent=2)+'\n')
