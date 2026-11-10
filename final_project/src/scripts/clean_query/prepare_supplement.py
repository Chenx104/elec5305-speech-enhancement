from pathlib import Path
import csv,json,hashlib,shutil,re,zipfile,xml.etree.ElementTree as E,argparse
W=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--project',type=Path,default=W.parents[2]);ap.add_argument('--run',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
P=a.project.resolve();B=a.run.resolve()if a.run else next((P/'runs').glob('experiment_*'))
R=a.output.resolve();assert not (R/'provenance.json').exists(),'Choose a fresh output directory.';R.mkdir(exist_ok=True,parents=True)
read=lambda p:list(csv.DictReader(Path(p).open()))
def write(p,rows):
 with Path(p).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for n in ['scripts','matlab','logs','dsp','dsp/audio16k']:(R/n).mkdir(exist_ok=True)
tools=(B/'test/tools').resolve()
fixed=json.loads((P/'protocol/reused_implementation_provenance.json').read_text())
for n,h in fixed['fixed_ECAPA_files_sha256'].items():assert sha(tools/'ecapa_model'/n)==h
assert sha(tools/'deep-filter-0.5.6-aarch64-apple-darwin')==fixed['fixed_DFN_binary_sha256']
assert sha(tools/'DeepFilterNet3_onnx.tar.gz')==fixed['fixed_DFN_model_archive_sha256']
if not (R/'tools').exists():(R/'tools').symlink_to(tools,target_is_directory=True)
conf=json.loads((B/'test/test_config.json').read_text());conf.update(split='clean_query_supplement',expected_mixtures=90,expected_clips=470)
(R/'test_config.json').write_text(json.dumps(conf,indent=2))
for n in ['run_deepfilter.py','extract_embeddings.py']:
 shutil.copy2(P/'src/scripts'/n,R/'scripts'/n)
# MATLAB helpers come from the supplied current MLX, not an older working copy.
z=zipfile.ZipFile(P/'final_project.mlx');tree=E.fromstring(z.read('matlab/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
code=[]
for p in tree.findall('.//w:body/w:p',ns):
 style=p.find('w:pPr/w:pStyle',ns)
 if style is not None and style.get('{'+ns['w']+'}val')=='code':code.append(''.join(t.text or ''for t in p.findall('.//w:t',ns)))
code='\n'.join(code);matches=list(re.finditer(r'^function\s+[^\n]*',code,re.M))
helpers={}
for i,m in enumerate(matches):
 head=m.group();name=re.search(r'(\w+)\s*\(',head).group(1)
 if name in ['p_stft','p_istft','p_noise_psd','p_spectral_gain','p_verification_metrics']:
  text=code[m.start():matches[i+1].start()if i+1<len(matches)else len(code)]
  # Strip only trailing source-description comments between functions.
  text=text.rstrip()+'\n';(R/'matlab'/(name+'.m')).write_text(text);helpers[name]=hashlib.sha256(text.encode()).hexdigest()
assert len(helpers)==5,helpers
C=read(B/'test/inputs/clean_index.csv');T=[r for r in C if r['RecordingRole']=='test'];refs=sorted([r for r in C if r['RecordingRole']=='enrollment_primary'],key=lambda r:r['SpeakerID'])
assert len(T)==90 and sum(r['ParticipantRole']=='target'for r in T)==60 and len(refs)==20
assert len({r['UtteranceID']for r in T})==90
assert not ({r['UtteranceID']for r in refs}&{r['UtteranceID']for r in T})
clipRows={r['ClipID']:r for r in read(B/'test/external/complete_clip_index.csv')}
audit={r['ClipID']:r['SHA256']for r in json.loads((B/'test/external/ecapa_audit.json').read_text())['clips']}
man=[];clips=[]
for r in refs+T:
 uid=r['UtteranceID'];raw=B/'test/inputs/clean'/(uid+'.wav');export=B/'test/dsp/audio16k'/('clean_'+uid+'.wav');cr=clipRows['clean_'+uid]
 assert sha(raw)==r['CleanSHA256'] and sha(export)==audit['clean_'+uid]
 dest=R/'dsp/audio16k'/export.name;shutil.copy2(export,dest)
 base={**cr,'Path':str(dest),'Method':'Clean'if r['RecordingRole']=='enrollment_primary'else 'Noisy','ConditionID':''if r['RecordingRole']=='enrollment_primary'else 'cleanprobe_'+uid}
 clips.append(base)
 man.append({**r,'CleanPath':str(raw),'ECAPAInputPath':str(dest),'ECAPAInputSHA256':sha(dest),'ExportGain':cr['ExportGain']})
write(R/'clean_manifest.csv',man);write(R/'dsp/base_clip_index.csv',clips)
selection=read(B/'development/results/development_selection.csv')[0];(R/'locked_selection.json').write_text(json.dumps(selection,indent=2))
provenance={'source_project':str(P),'source_run':str(B),'source_mlx_sha256':sha(P/'final_project.mlx'),'source_embeddings_sha256':sha(B/'test/external/embeddings.npz'),'helpers_from_current_mlx':helpers,'protocol':'90 unique clean test queries; 20 unchanged primary enrollment; no threshold retuning; main-run noisy test not modified','query_processing':'Use exact pre-mixture 5 s FLOAT crops (peak 0.7); original common export gain and PCM24. Baseline input identical by SHA256 to clean files already embedded in main run. SS receives only its input speech, no oracle noise PSD.'}
(R/'provenance.json').write_text(json.dumps(provenance,indent=2));print('PREPARED',len(man),'recordings',helpers)
