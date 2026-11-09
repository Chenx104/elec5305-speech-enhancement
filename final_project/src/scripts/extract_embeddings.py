"""Extract fixed ECAPA embeddings for every clip; always recompute."""
import os
os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_XET']='1'
from pathlib import Path
import csv,json,time,hashlib,importlib.metadata,sys
import numpy as np,soundfile as sf,torch
from speechbrain.inference.speaker import EncoderClassifier
R=Path(sys.argv[1]).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 C=json.loads((R/'test_config.json').read_text());rows=list(csv.DictReader((R/'external/complete_clip_index.csv').open()));assert len(rows)==C['expected_clips'];cache=R/'tools/ecapa_model';revision=json.loads((cache/'model_revision.json').read_text());assert revision['revision']=='0f99f2d0ebe89ac095bcc5903c4dd8f72b367286'
 torch.set_num_threads(C['threads']);torch.manual_seed(C['seed']);torch.use_deterministic_algorithms(True)
 model=EncoderClassifier.from_hparams(source=str(cache),savedir=str(R/'external/ecapa_loaded'),overrides={'pretrained_path':str(cache)},run_opts={'device':'cpu'});model.mods.eval()
 for module in model.mods.values():
  for param in module.parameters():param.requires_grad_(False)
 embeddings=[];provenance=[];start=time.perf_counter()
 for i,r in enumerate(rows):
  p=Path(r['Path']);x,sr=sf.read(p,dtype='float32');assert sr==16000 and x.shape==(80000,) and np.isfinite(x).all()
  with torch.inference_mode():e=model.encode_batch(torch.from_numpy(x.copy()).unsqueeze(0)).squeeze().cpu().numpy()
  assert e.shape==(192,) and np.isfinite(e).all() and np.linalg.norm(e)>0
  embeddings.append(e.copy());provenance.append({'ClipID':r['ClipID'],'SHA256':sha(p)})
  if (i+1)%80==0 or i+1==len(rows):print(f'ECAPA {i+1}/{len(rows)}',flush=True)
 np.savez_compressed(R/'external/embeddings.npz',clip_ids=np.array([r['ClipID'] for r in rows]),embeddings=np.array(embeddings))
 meta={'revision':revision,'device':'cpu','threads':C['threads'],'seed':C['seed'],'clips':provenance,'elapsed_seconds':time.perf_counter()-start,'packages':{n:importlib.metadata.version(n) for n in ['torch','torchaudio','speechbrain','numpy','scipy','soundfile']}}
 (R/'external/ecapa_audit.json').write_text(json.dumps(meta,indent=2)+'\n');print('ECAPA_COMPLETE',flush=True)
if __name__=='__main__':main()
