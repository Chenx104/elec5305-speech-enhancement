"""Material preparation only: five disjoint four-reader babble sources."""
import io,csv,json,hashlib,tarfile
from pathlib import Path
import numpy as np,soundfile as sf
r=Path(__file__).resolve().parent;base=r.parent;roles=list(csv.DictReader((base/'material_audit/candidate_speaker_roles.csv').open()));background=[z for z in roles if z['BabbleGroup']];needed={z['SpeakerID'] for z in background};data={s:[] for s in needed};fs=16000;join=160;track_need=330*fs;length={s:0 for s in needed};details={s:[] for s in needed}
with tarfile.open(base/'material_audit/dev-clean.tar.gz','r|gz') as tar:
 for member in tar:
  if not member.isfile() or not member.name.endswith('.flac'):continue
  uid=Path(member.name).stem;sp=uid.split('-')[0]
  if sp not in needed or length[sp]>=track_need:continue
  blob=tar.extractfile(member).read();x,sr=sf.read(io.BytesIO(blob));assert sr==fs and x.ndim==1 and np.isfinite(x).all();x=x-x.mean();assert np.max(abs(x))>0
  data[sp].append((uid,x));length[sp]+=len(x)-(join if len(data[sp])>1 else 0);details[sp].append({'UtteranceID':uid,'ArchiveMember':member.name,'SourceSHA256':hashlib.sha256(blob).hexdigest()})
assert all(length[s]>=track_need for s in needed)
# Archive traversal order is recorded verbatim, not inferred to be numeric order.
tracks={}
for sp,parts in data.items():
 y=parts[0][1].copy();ramp=np.linspace(0,1,join,endpoint=True)
 for uid,x in parts[1:]:y=np.r_[y[:-join],y[-join:]*(1-ramp)+x[:join]*ramp,x[join:]]
 assert len(y)>=track_need;tracks[sp]=y
folder=r/'babble';folder.mkdir(exist_ok=True);records=[]
for gi,group in enumerate(sorted({z['BabbleGroup'] for z in background})):
 members=sorted([z for z in background if z['BabbleGroup']==group],key=lambda z:int(z['SpeakerID']));assert len(members)==4 and sorted(z['Sex'] for z in members)==['F','F','M','M'];rng=np.random.default_rng(np.random.SeedSequence([530803,gi]));signals=[];inputs=[]
 for row in members:
  sp=row['SpeakerID'];track=tracks[sp];offset=int(rng.integers(0,min(len(track)-300*fs,30*fs)+1));x=track[offset:offset+300*fs];assert len(x)==300*fs;x=x-x.mean();x=x/np.sqrt(np.mean(x*x));signals.append(x);inputs.append({'SpeakerID':sp,'Sex':row['Sex'],'StartSampleInConcatenatedTrack':offset,'SourceUtterancesInArchiveOrder':details[sp]})
 y=np.sum(signals,axis=0)/4;y=.9*y/np.max(abs(y));path=folder/('BABBLE_'+group+'.wav');sf.write(path,y,fs,subtype='FLOAT');rec={'SourceID':'BABBLE_'+group,'Split':'development' if group.startswith('dev') else 'test','Class':'Babble','SampleRate':fs,'Duration_s':300,'People':4,'Males':2,'Females':2,'JoinCrossfade_samples':join,'SeedBase':530803,'StreamIndex':gi,'Inputs':inputs,'SourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'Path':str(path.resolve())};records.append(rec);print(rec['SourceID'],'300 s, 2M/2F, independent group',flush=True)
(r/'babble_provenance.json').write_text(json.dumps(records,indent=2));print('Five babble sources prepared without running any learned model.',flush=True)
