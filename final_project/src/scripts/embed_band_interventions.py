"""CPU-only, offline, frozen ECAPA embeddings for allowed development/enrollment files."""
import os
os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_XET']='1'
import csv,json,time,hashlib,importlib.metadata
from pathlib import Path
import numpy as np,soundfile as sf,torch
from speechbrain.inference.speaker import EncoderClassifier
import sys
R=Path(sys.argv[1]).resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
 C=json.loads((R/'test_config.json').read_text());index=R/'band_intervention/clip_index.csv';rows=list(csv.DictReader(index.open()));assert len(rows)>0 and len(rows)%31==0
 assert len({r['UtteranceID'] for r in rows})*31==len(rows) and all(r['Kind'] in ['clean','fixed','fixed_level_control','matched','matched_level_control'] for r in rows)
 cache=R/'tools/ecapa_model';revision=json.loads((cache/'model_revision.json').read_text());assert revision['revision']=='0f99f2d0ebe89ac095bcc5903c4dd8f72b367286'
 torch.set_num_threads(C['threads']);torch.manual_seed(C['seed']);torch.use_deterministic_algorithms(True)
 model=EncoderClassifier.from_hparams(source=str(cache),savedir=str(R/'band_intervention/ecapa_loaded'),overrides={'pretrained_path':str(cache)},run_opts={'device':'cpu'});model.mods.eval()
 for module in model.mods.values():
  for p in module.parameters():p.requires_grad_(False)
 embeddings=[];provenance=[];t=time.time();repeat=None
 for i,r in enumerate(rows):
  p=Path(r['Path']);x,sr=sf.read(p,dtype='float32');assert sr==16000 and x.shape==(80000,) and np.isfinite(x).all()
  with torch.inference_mode():e=model.encode_batch(torch.from_numpy(x.copy()).unsqueeze(0)).squeeze().cpu().numpy()
  assert e.shape==(192,) and np.isfinite(e).all() and np.linalg.norm(e)>0
  if i==0:
   with torch.inference_mode():e2=model.encode_batch(torch.from_numpy(x.copy()).unsqueeze(0)).squeeze().cpu().numpy()
   repeat=float(np.max(abs(e-e2)));assert repeat==0
  embeddings.append(e.copy());provenance.append({'ClipID':r['ClipID'],'SHA256':sha(p)})
  if (i+1)%100==0 or i+1==len(rows):print(f'ECAPA {i+1}/{len(rows)}; {time.time()-t:.1f}s',flush=True)
 np.savez_compressed(R/'band_intervention/embeddings.npz',clip_ids=np.array([r['ClipID'] for r in rows]),embeddings=np.array(embeddings))
 meta={'revision':revision,'device':'cpu','threads':C['threads'],'seed':C['seed'],'deterministic_algorithms':True,'repeat_first_embedding_max_abs_error':repeat,'clips':provenance,'index_sha256':sha(index),'model_files_sha256':{n:sha(cache/n) for n in revision['files']},'packages':{n:importlib.metadata.version(n) for n in ['torch','torchaudio','speechbrain','numpy','scipy','soundfile']},'test_processed':True,'elapsed_seconds':time.time()-t}
 (R/'band_intervention/ecapa_audit.json').write_text(json.dumps(meta,indent=2)+'\n');print('TEST_ECAPA_COMPLETE',flush=True)
