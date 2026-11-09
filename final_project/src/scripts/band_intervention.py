"""Predeclared clean-speech band perturbations; no identity model or fitting."""
import numpy as np
FS=16000
BANDS=((0.,1000.),(1000.,3000.),(3000.,8000.))

def band_mask(freq,lo,hi,transition=50.):
 # Interior bands cross-fade symmetrically within +/-25 Hz of a boundary.
 m=np.ones_like(freq)
 if lo>0:
  t=np.clip((freq-(lo-transition/2))/transition,0,1);m*=.5-.5*np.cos(np.pi*t)
 if hi<FS/2:
  t=np.clip((freq-(hi-transition/2))/transition,0,1);m*=.5+.5*np.cos(np.pi*t)
 return m

def attenuate(x,band,attenuation_db):
 x=np.asarray(x,dtype=float);assert x.ndim==1 and len(x)==80000
 pad=FS;v=np.pad(x,(pad,pad),mode='reflect');f=np.fft.rfftfreq(len(v),1/FS);m=band_mask(f,*band)
 h=1-(1-10**(-attenuation_db/20))*m
 return np.fft.irfft(np.fft.rfft(v)*h,n=len(v))[pad:-pad]

def perturbations(x,attenuation_db):
 x=np.asarray(x,dtype=float);assert np.isfinite(x).all() and np.dot(x,x)>0
 fixed=[attenuate(x,b,attenuation_db) for b in BANDS];energy=np.dot(x,x)
 # Equal-energy controls use the SMALLEST nonnegative energy loss achievable
 # among the three bands at this level; therefore no band needs amplification.
 e=np.array([np.dot(z,z) for z in fixed]);target=min(energy,float(e.max()));matched=[];effective=[]
 for band,z in zip(BANDS,fixed):
  if np.dot(z,z)>=target:
   a=attenuation_db;zz=z
  else:
   lo,hi=0.,float(attenuation_db)
   for _ in range(55):
    a=(lo+hi)/2;zz=attenuate(x,band,a)
    if np.dot(zz,zz)>target:lo=a
    else:hi=a
   a=(lo+hi)/2;zz=attenuate(x,band,a)
  assert abs(np.dot(zz,zz)-target)/energy<1e-9
  matched.append(zz);effective.append(a)
 return {'fixed':fixed,'fixed_whole_level_controls':[x*np.sqrt(float(z@z)/energy) for z in fixed],'energy_matched':matched,'matched_attenuation_db':effective,'whole_level_control':x*np.sqrt(target/energy),'energy_ratio':target/energy}

def checks():
 t=np.arange(80000)/FS;x=sum(np.sin(2*np.pi*f*t) for f in [500,2000,5000])/3
 out=perturbations(x,6)
 for zs in [out['fixed'],out['energy_matched']]:assert all(np.isfinite(z).all() and len(z)==80000 for z in zs)
 energies=[np.dot(z,z) for z in out['energy_matched']]+[np.dot(out['whole_level_control'],out['whole_level_control'])]
 assert (max(energies)-min(energies))/np.dot(x,x)<1e-9
 assert max(abs(attenuate(x,BANDS[0],0)-x))<1e-12
 for z,c in zip(out['fixed'],out['fixed_whole_level_controls']):assert abs(float(z@z)-float(c@c))/float(x@x)<1e-12
 return {'identity_at_zero_attenuation':True,'equal_energy_controls_verified':True,'length_and_finite':True}
if __name__=='__main__':print(checks())
