"""Fetch only channel 01 from each official DEMAND ZIP via verified HTTP ranges.
ZIP member CRC is checked; this does NOT claim a full-archive MD5 verification.
"""
import io,json,struct,zipfile,zlib,time,hashlib,csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests,soundfile as sf
r=Path(__file__).resolve().parent;j=json.loads((r/'zenodo_record.json').read_text());files={x['key']:x for x in j['files']};envs=sorted({k.split('_')[0] for k in files if k.endswith(('_16k.zip','_48k.zip'))});raw=r/'raw_ch01';raw.mkdir(exist_ok=True)
def fetch_range(session,url,start,end):
 assert 0<=start<=end
 for attempt in range(5):
  q=session.get(url,params={'audit_range':f'{start}-{end}'},headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},timeout=(20,120))
  if q.status_code in [429,500,502,503,504]:time.sleep(min(30,2**attempt));continue
  q.raise_for_status();expected=f'bytes {start}-{end}/';assert q.status_code==206 and q.headers.get('Content-Range','').startswith(expected),(q.status_code,q.headers.get('Content-Range'));assert len(q.content)==end-start+1;return q.content
 raise RuntimeError('Range retries exhausted: '+url)
def one(env):
 key=env+('_16k.zip' if env+'_16k.zip' in files else '_48k.zip');meta=files[key];url=meta['links']['self'];size=meta['size'];session=requests.Session();tailstart=max(0,size-131072);tail=fetch_range(session,url,tailstart,size-1);pos=tail.rfind(b'PK\x05\x06');assert pos>=0;values=list(struct.unpack('<4s4H2LH',tail[pos:pos+22]));cdsize,offset=values[5],values[6];assert values[1]==values[2]==0 and values[3]==values[4] and values[4]<65535
 cd=tail[offset-tailstart:offset-tailstart+cdsize] if offset>=tailstart else fetch_range(session,url,offset,offset+cdsize-1);assert len(cd)==cdsize
 values[6]=0;values[7]=0
 with zipfile.ZipFile(io.BytesIO(cd+struct.pack('<4s4H2LH',*values))) as z:
  names=z.namelist();members=[x for x in z.infolist() if Path(x.filename).name.lower()=='ch01.wav'];assert len(members)==1,(env,names);info=members[0]
 header=fetch_range(session,url,info.header_offset,info.header_offset+29);h=struct.unpack('<4s5H3L2H',header);assert h[0]==b'PK\x03\x04';start=info.header_offset+30+h[-2]+h[-1];compressed=fetch_range(session,url,start,start+info.compress_size-1)
 data=zlib.decompress(compressed,-15) if info.compress_type==zipfile.ZIP_DEFLATED else compressed if info.compress_type==zipfile.ZIP_STORED else None;assert data is not None and len(data)==info.file_size;assert zlib.crc32(data)&0xffffffff==info.CRC
 audioinfo=sf.info(io.BytesIO(data));assert audioinfo.channels==1 and audioinfo.samplerate in [16000,48000];dest=raw/(env+'_ch01_'+str(audioinfo.samplerate)+'.wav');dest.write_bytes(data)
 record={'Environment':env,'Archive':key,'OfficialArchiveChecksum':meta.get('checksum'),'ArchiveURL':url,'ArchiveSize':size,'Member':info.filename,'MemberCRC32':f'{info.CRC:08x}','MemberCRCVerified':True,'FullArchiveMD5Verified':False,'SourceSHA256':hashlib.sha256(data).hexdigest(),'NativeSampleRate':audioinfo.samplerate,'Samples':audioinfo.frames,'Duration_s':audioinfo.duration,'Path':str(dest.resolve()),'CentralDirectorySHA256':hashlib.sha256(cd).hexdigest()};(r/(env+'_retrieval.json')).write_text(json.dumps(record,indent=2));print(f'{env}: ch01 {audioinfo.samplerate} Hz, {audioinfo.duration:.3f} s, CRC verified',flush=True);return record
records=[]
with ThreadPoolExecutor(max_workers=3) as pool:
 for f in as_completed([pool.submit(one,e) for e in envs]):records.append(f.result())
records.sort(key=lambda z:z['Environment']);(r/'channel01_inventory.json').write_text(json.dumps(records,indent=2))
with (r/'channel01_inventory.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print('DONE',len(records),'environments; 16-kHz archives',sum(z['NativeSampleRate']==16000 for z in records),flush=True)
