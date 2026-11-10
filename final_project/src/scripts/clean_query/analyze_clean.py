from pathlib import Path
import csv,json,hashlib,argparse
import numpy as np
from scipy.io import savemat
W=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=W/'experiment');args=ap.parse_args();R=args.root.resolve()
read=lambda p:list(csv.DictReader(Path(p).open()))
def write(p,rows):
 with Path(p).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def metrics(scores,genuine,threshold):
 s=np.asarray(scores,dtype=np.float64);g=np.asarray(genuine,dtype=bool)
 accepted=s>=threshold;ng=g.sum();ni=(~g).sum()
 far=np.sum(accepted&~g)/ni;frr=np.sum(~accepted&g)/ng
 order=np.argsort(-s,kind='stable');ss=s[order];gg=g[order]
 ends=np.r_[np.flatnonzero(np.diff(ss)!=0),len(ss)-1]
 fars=np.r_[0,np.cumsum(~gg)[ends]/ni];frrs=np.r_[1,1-np.cumsum(gg)[ends]/ng]
 delta=fars-frrs;hi=np.flatnonzero(delta>=0)[0];lo=max(0,hi-1)
 if delta[hi]==0:eer=(fars[hi]+frrs[hi])/2
 else:eer=fars[lo]+(-delta[lo]/(delta[hi]-delta[lo]))*(fars[hi]-fars[lo])
 return dict(EER_pct=100*eer,FAR_pct=100*far,FRR_pct=100*frr,BER_pct=50*(far+frr),GenuineTrials=int(ng),ExternalTrials=int(ni),FalseRejects=int(np.sum(~accepted&g)),FalseAccepts=int(np.sum(accepted&~g)),Threshold=threshold)
def main():
 prov=json.loads((R/'provenance.json').read_text());B=Path(prov['source_run']);M=read(R/'clean_manifest.csv')
 Q=[r for r in M if r['RecordingRole']=='test'];refs=sorted([r for r in M if r['RecordingRole']=='enrollment_primary'],key=lambda r:r['SpeakerID'])
 old=np.load(B/'test/external/embeddings.npz');oldmap={str(i):np.asarray(e,dtype=np.float64)for i,e in zip(old['clip_ids'],old['embeddings'])}
 threshold=float(json.loads((R/'locked_selection.json').read_text())['Noisy_development_threshold'])
 new=R/'external/embeddings.npz'
 if new.exists():
  z=np.load(new);emb={str(i):np.asarray(e,dtype=np.float64)for i,e in zip(z['clip_ids'],z['embeddings'])}
  dif=max(float(np.max(abs(emb['clean_'+r['UtteranceID']]-oldmap['clean_'+r['UtteranceID']])))for r in M)
  assert dif<1e-5,('Cached vs fresh embedding discrepancy',dif)
  methods=['Clean','Clean_SS_a1p5','Clean_DeepFilterNet','Clean_Resample_only','Clean_Adapter']
 else:emb=oldmap;dif=None;methods=['Clean']
 def unit(x):return x/np.linalg.norm(x,axis=-1,keepdims=True)
 refE=unit(np.stack([oldmap['clean_'+r['UtteranceID']]for r in refs]))
 scores=[];gen=[];methodrows=[];trialrows=[];pairrows=[];arrays={};baseline=None
 for method in methods:
  ids=['clean_'+r['UtteranceID']if method=='Clean'else 'cleanprobe_'+r['UtteranceID']+'_'+method.removeprefix('Clean_')for r in Q]
  E=unit(np.stack([emb[i]for i in ids]));S=E@refE.T
  target=np.array([r['ParticipantRole']=='target'for r in Q]);same=np.array([r['SpeakerID']for r in Q])[:,None]==np.array([r['SpeakerID']for r in refs])[None,:]
  genuine=target[:,None]&same;external=np.broadcast_to((~target)[:,None],S.shape);mask=genuine|external
  assert genuine.sum()==60 and external.sum()==600
  v=S[mask];g=genuine[mask];m=metrics(v,g,threshold)
  methodrows.append({'Method':method,**m,'MeanGenuineScore':float(np.mean(S[genuine])),'MeanExternalScore':float(np.mean(S[external])),'MinimumGenuineScore':float(np.min(S[genuine])),'MaximumExternalScore':float(np.max(S[external]))})
  if method=='Clean':baseline=S.copy()
  for qi,r in enumerate(Q):
   for ri,ref in enumerate(refs):
    if not mask[qi,ri]:continue
    trialrows.append(dict(Method=method,UtteranceID=r['UtteranceID'],SpeakerID=r['SpeakerID'],ReferenceSpeakerID=ref['SpeakerID'],TrialType='genuine'if genuine[qi,ri]else'external',Score=float(S[qi,ri]),Accepted=bool(S[qi,ri]>=threshold),CleanScore=float(baseline[qi,ri]),ScoreChange=float(S[qi,ri]-baseline[qi,ri])))
  scores.append(v);gen.append(g);arrays[method]=S
  if method!='Clean':
   for label,mask2 in [('genuine',genuine),('external',external)]:
    b=baseline[mask2]>=threshold;a=S[mask2]>=threshold;correct=lambda accepted:accepted if label=='genuine'else ~accepted
    bc=correct(b);ac=correct(a);pairrows.append(dict(Method=method,TrialType=label,Trials=int(mask2.sum()),Correct_to_Wrong=int(np.sum(bc&~ac)),Wrong_to_Correct=int(np.sum(~bc&ac)),MeanScoreChange=float(np.mean(S[mask2]-baseline[mask2]))))
 write(R/'clean_query_summary.csv',methodrows);write(R/'clean_query_trials.csv',trialrows)
 if pairrows:write(R/'paired_decision_changes.csv',pairrows)
 np.savez_compressed(R/'clean_query_scores.npz',**arrays)
 savemat(R/'metric_check.mat',dict(scores=np.stack(scores,axis=1),genuine=gen[0].astype(np.uint8)[:,None],threshold=threshold,method_names=np.array(methods,dtype=object),expected=np.array([[r[k]for k in ['EER_pct','FAR_pct','FRR_pct','BER_pct']]for r in methodrows])))
 # Reproduce the original main-run primary results from cached embeddings.
 conditions=read(B/'test/inputs/test_conditions.csv');original=[]
 for method in ['Noisy','SS_a1p5','DeepFilterNet']:
  ee=unit(np.stack([oldmap[r['ConditionID']+'_'+method]for r in conditions]));S=ee@refE.T
  t=np.array([r['ParticipantRole']=='target'for r in conditions]);same=np.array([r['SpeakerID']for r in conditions])[:,None]==np.array([r['SpeakerID']for r in refs])[None,:]
  g=t[:,None]&same;ext=np.broadcast_to((~t)[:,None],S.shape);mask=g|ext;v=metrics(S[mask],g[mask],threshold)
  assert v['GenuineTrials']==720 and v['ExternalTrials']==7200
  original.append({'Method':method,**v})
 write(R/'main_run_reproduced.csv',original)
 expected={'Noisy':7.08333333333333,'SS_a1p5':8.76388888888889,'DeepFilterNet':9.02777777777778}
 for r in original:assert abs(r['EER_pct']-expected[r['Method']])<1e-8,r
 report={'clean_unique_target_utterances':60,'clean_unique_external_utterances':30,'primary_references':20,'common_threshold':threshold,'threshold_reselected':False,'same_queries_replicated':False,'fresh_vs_cached_clean_embedding_max_absolute_difference':dif,'main_EER_reproduced':True,'methods_complete':methods,'results':methodrows,'main_results':original,'comparison_scope':'Clean vs main Noisy is descriptive (different condition weights and trial counts); no causal artifact attribution and no new confidence interval claimed.'}
 (R/'analysis_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
