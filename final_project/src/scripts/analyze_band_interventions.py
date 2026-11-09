"""Compare frozen band perturbations with their energy-matched level controls."""
from pathlib import Path
import csv,json
import numpy as np
import sys
R=Path(sys.argv[1]).resolve()
def write(p,rows):
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if __name__=='__main__':
 D=R/'band_intervention';rows=list(csv.DictReader((D/'clip_index.csv').open()));Z=np.load(D/'embeddings.npz');assert list(Z['clip_ids'])==[r['ClipID'] for r in rows];E=Z['embeddings'].astype(float);E/=np.linalg.norm(E,axis=1,keepdims=True);lookup=dict(zip(Z['clip_ids'],E));result=[]
 for r in rows:
  if r['Kind']=='clean':continue
  uid=r['UtteranceID'];ref=lookup[f'band_{uid}_clean_0_-1'];vec=lookup[r['ClipID']];delta=float(ref@vec-ref@ref);level=int(float(r['Level_dB']));bi=int(r['BandIndex']);kind=r['Kind'];control_delta=np.nan
  if kind in ['fixed','matched']:
   control=f'band_{uid}_fixed_level_control_{level}_{bi}' if kind=='fixed' else f'band_{uid}_matched_level_control_{level}_-1';control_delta=float(ref@lookup[control]-ref@ref)
  result.append({k:r[k] for k in ['ClipID','SpeakerID','UtteranceID','Kind','Level_dB','BandIndex','BandLow_Hz','BandHigh_Hz','EffectiveAttenuation_dB','EnergyRatio','ExportGain']}|{'DeltaCosToUnprocessed':delta,'LevelControlDeltaCos':control_delta,'DifferenceFromLevelControl':delta-control_delta})
 write(R/'results/band_intervention_results.csv',result);summary=[]
 for kind in ['fixed','matched']:
  for level in [3,6,12]:
   for bi in range(3):
    rr=[r for r in result if r['Kind']==kind and float(r['Level_dB'])==level and int(r['BandIndex'])==bi];assert len(rr)>0
    summary.append({'Kind':kind,'Level_dB':level,'BandIndex':bi,'BandLow_Hz':rr[0]['BandLow_Hz'],'BandHigh_Hz':rr[0]['BandHigh_Hz'],'Utterances':len(rr),'Speakers':len({r['SpeakerID'] for r in rr}),'MeanDeltaCos':float(np.mean([r['DeltaCosToUnprocessed'] for r in rr])),'MeanLevelControlDeltaCos':float(np.mean([r['LevelControlDeltaCos'] for r in rr])),'MeanDifferenceFromLevelControl':float(np.mean([r['DifferenceFromLevelControl'] for r in rr])),'MeanEnergyRatio':float(np.mean([float(r['EnergyRatio']) for r in rr])),'MinimumEffectiveAttenuation_dB':min(float(r['EffectiveAttenuation_dB']) for r in rr),'MeanEffectiveAttenuation_dB':float(np.mean([float(r['EffectiveAttenuation_dB']) for r in rr])),'MaximumEffectiveAttenuation_dB':max(float(r['EffectiveAttenuation_dB']) for r in rr)})
 write(R/'results/band_intervention_summary.csv',summary)
 print('Band intervention descriptive analysis complete: 60 utterances,20 speakers; no model tuning.')
