"""Rebuild all report figures from the accompanying verified source_data files."""
from pathlib import Path
import csv,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
D=Path(__file__).resolve().parents[1];S=D/'source_data';F=D/'figures';QA=D/'qa';F.mkdir(exist_ok=True);QA.mkdir(exist_ok=True)
# Optional audit helper; figure generation remains portable when it is absent.
try:from audit_panel_alignment import require_matplotlib_panel_alignment
except ImportError:require_matplotlib_panel_alignment=None
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':8,'axes.labelsize':8,'axes.titlesize':8,'legend.fontsize':7,'xtick.labelsize':7,'ytick.labelsize':7,'pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'lines.linewidth':1.2,'savefig.dpi':300})
C={'Noisy':'#555555','SS_a0p5':'#72983f','SS_a1p5':'#2778ad','SS_a3p0':'#8b66b0','DeepFilterNet':'#cf6f32','VAD_SS':'#bd5555','Tracking_SS':'#519c97'}
L={'Noisy':'Noisy','SS_a0p5':'SS 0.5','SS_a1p5':'SS 1.5','SS_a3p0':'SS 3','DeepFilterNet':'DeepFilterNet','VAD_SS':'VAD-SS','Tracking_SS':'Tracking-SS'}
read=lambda n:list(csv.DictReader((S/n).open()))
summary={r['Method']:r for r in read('overall_results.csv')};dev={r['Method']:r for r in read('development_summary.csv') if r['ReferenceSet']=='enrollment_primary'}
def save(fig,name,axes=None):
 fig.canvas.draw()
 if require_matplotlib_panel_alignment:
  opts={} if axes is None else {'exclude_axes':[a for a in fig.axes if a not in axes]}
  require_matplotlib_panel_alignment(fig,json_out=QA/(name+'.alignment.json'),strict=True,**opts)
 else:
  (QA/(name+'.alignment.json')).write_text(json.dumps({'status':'not run','reason':'optional alignment helper unavailable'}))
 fig.savefig(F/(name+'.pdf'),bbox_inches='tight',pad_inches=.035);fig.savefig(QA/(name+'.svg'),bbox_inches='tight',pad_inches=.035);fig.savefig(QA/(name+'.png'),bbox_inches='tight',pad_inches=.035,dpi=300);plt.close(fig)
def panel(ax,label):ax.text(0,1.05,label,transform=ax.transAxes,fontweight='bold',fontsize=8)
# Fig. 1: same-utterance clean and separate enrollment references have different roles.
fig,ax=plt.subplots(figsize=(7.16,2.55));ax.set_xlim(0,10);ax.set_ylim(0,5);ax.axis('off')
def box(x,y,w,h,text,color='#edf2f6'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.035',fc=color,ec='#657681',lw=.8));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=7.6)
def arrow(a,b,style='-'):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=9,lw=.9,color='#465560',linestyle=style,connectionstyle='arc3'))
box(.08,2.58,1.85,.88,'Same-utterance\nclean speech');box(.08,1.02,1.85,.78,'Fixed noise\nsegment');box(2.5,2.58,1.6,.88,'Mix at\n−5 / 0 / 5 / 10 dB');box(4.62,2.58,1.65,.88,'Systems\nNoisy / SS / DFN');box(7.05,3.62,2.7,.83,'SI-SDR, STOI and\nsame-utterance Δcos');box(7.05,2.10,2.7,.83,'ECAPA + cosine scoring\nEER, FAR, FRR, BER');box(4.62,.57,2.25,.83,'Separate clean\nenrollment recording',color='#f8eedf');box(2.6,4.08,3.7,.64,'Development selects α and thresholds',color='#eef4e9')
for a,b in [((1.93,3.02),(2.5,3.02)),((1.93,1.4),(2.5,2.78)),((4.1,3.02),(4.62,3.02)),((6.27,3.12),(7.05,4.03)),((6.27,2.82),(7.05,2.52)),((6.87,.99),(7.45,2.1)),((4.45,4.08),(5.3,3.46))]:arrow(a,b)
ax.plot([1.03,1.03,8.45],[3.46,4.94,4.94],color='#657681',lw=.85);arrow((8.45,4.94),(8.45,4.45));ax.text(8.2,.18,'Test: no parameter tuning',ha='center',fontsize=7.1)
save(fig,'experimental_pipeline')
# Fig. 2: α controls two objectives, with choices made on development only.
alphas=[.5,1,1.5,2,3];methods=['SS_a0p5','SS_a1p0','SS_a1p5','SS_a2p0','SS_a3p0'];q=np.array([float(summary[m]['TargetSI_SDRGain_dB']) for m in methods]);e=np.array([float(summary[m]['ExternalEER_pct']) for m in methods])
fig,axs=plt.subplots(1,2,figsize=(7.16,2.35));fig.subplots_adjust(left=.075,right=.985,bottom=.24,top=.87,wspace=.34)
a=axs[0];a.plot(alphas,[float(dev[m]['ExternalEER_pct']) for m in methods],'--o',c='#888888',label='Development');a.plot(alphas,e,'-o',c=C['SS_a1p5'],label='Test');a.set(xlabel='Subtraction strength α',ylabel='External-verification EER (%)',xticks=alphas);a.legend(loc='upper left');panel(a,'(a)')
a=axs[1];a.plot(q,e,'-o',c=C['SS_a1p5']);a.scatter(q[[0,4]],e[[0,4]],marker='s',s=32,c=[C['SS_a0p5'],C['SS_a3p0']],zorder=4)
for x,y,t in zip(q,e,alphas):a.annotate(str(t),(x,y),xytext=((-8,8) if t==.5 else (4,-10 if t<3 else -12)),textcoords='offset points',fontsize=7)
a.set(xlabel='Test SI-SDR gain (dB)',ylabel='External-verification EER (%)',xlim=(.3,1.48),ylim=(7.1,10.1));panel(a,'(b)');save(fig,'alpha_analysis',list(axs))
# Fig. 3: pooled SNR effects and paired source differences, not source averages of EER.
cond=read('conditional_verification.csv');sources=read('source_verification.csv');main=['Noisy','SS_a0p5','SS_a1p5','SS_a3p0','DeepFilterNet'];fig,axs=plt.subplots(1,2,figsize=(7.16,2.85));fig.subplots_adjust(left=.075,right=.985,bottom=.21,top=.9,wspace=.60)
for m in main:
 r=sorted([r for r in cond if r['Method']==m and r['NoiseClass']=='ALL'],key=lambda z:float(z['InputSNR_dB']));axs[0].plot([float(z['InputSNR_dB']) for z in r],[float(z['EER_pct']) for z in r],'-o',c=C[m],label=L[m],ms=3)
axs[0].set(xlabel='Input SNR (dB)',ylabel='External-verification EER (%)',xticks=[-5,0,5,10]);axs[0].legend(loc='upper right',fontsize=6.7);panel(axs[0],'(a)')
order=['NRIVER','TCAR','PRESTO','STRAFFIC','OMEETING','TMETRO','BABBLE_test_1','BABBLE_test_2','BABBLE_test_3'];base={r['NoiseSourceID']:float(r['EER_pct']) for r in sources if r['Method']=='Noisy'}
for j,m in enumerate(['SS_a1p5','DeepFilterNet']):
 vals={r['NoiseSourceID']:float(r['EER_pct'])-base[r['NoiseSourceID']] for r in sources if r['Method']==m};axs[1].scatter([vals[k] for k in order],np.arange(9)+(j-.5)*.20,c=C[m],s=19,label=L[m])
axs[1].axvline(0,c='#999999',lw=.7);axs[1].set(yticks=np.arange(9),yticklabels=[x.replace('BABBLE_test_','Babble ') for x in order],xlabel='EER difference from Noisy (pp)');axs[1].invert_yaxis();axs[1].legend(loc='lower right',fontsize=6.7);panel(axs[1],'(b)');save(fig,'noise_conditions',list(axs))
# Fig. 4: all 720 target mixtures for each of the four main enhanced systems.
cases=read('case_assignments.csv');fig,ax=plt.subplots(figsize=(3.48,2.55));fig.subplots_adjust(left=.19,right=.985,bottom=.20,top=.95)
for m in ['SS_a0p5','SS_a1p5','SS_a3p0','DeepFilterNet']:
 r=[z for z in cases if z['Method']==m];ax.scatter([float(z['SI_SDRGain_dB']) for z in r],[float(z['DeltaCos']) for z in r],s=5,alpha=.40,c=C[m],label=L[m],rasterized=True,linewidths=0)
ax.axvline(1,c='#999999',lw=.7,ls='--');ax.axhline(.01,c='#999999',lw=.7,ls='--');ax.axhline(-.01,c='#999999',lw=.7,ls='--');ax.set(xlabel='SI-SDR gain (dB)',ylabel='Enhancement Δcos');ax.legend(loc='lower right',markerscale=2,fontsize=6.7);save(fig,'embedding_analysis')
# Fig. 5: time-domain component retention, not bandwise STFT-energy retention.
metrics=read('overall_results.csv');raw=read('target_component_metrics.csv');lookup={(z['ConditionID'],z['Method']):float(z['DeltaCos']) for z in cases}
fig,ax=plt.subplots(figsize=(3.48,2.50));fig.subplots_adjust(left=.19,right=.985,bottom=.20,top=.95)
for m in ['SS_a1p5','VAD_SS','Tracking_SS']:
 r=[z for z in raw if z['Method']==m and z['ParticipantRole']=='target'];ax.scatter([float(z['SpeechRetained_pct']) for z in r],[lookup[z['ConditionID'],m] for z in r],s=5,alpha=.40,c=C[m],label=L[m],rasterized=True,linewidths=0)
ax.set(xlabel='Retained speech energy (%)',ylabel='Enhancement Δcos');ax.legend(loc='lower right',markerscale=2,fontsize=6.7);save(fig,'speech_retention')
# Fig. 6: a fixed representative; the common color scale is referenced to Noisy.
z=np.load(S/'failure_case_spectra.npz');fig,axs=plt.subplots(1,4,figsize=(7.16,2.00),sharex=True,sharey=True);fig.subplots_adjust(left=.065,right=.905,bottom=.24,top=.88,wspace=.15)
for i,(ax,title) in enumerate(zip(axs,['Clean','Noisy','SS 1.5','DeepFilterNet'])):
 im=ax.pcolormesh(z['time'],z['frequency']/1000,z['spectra_db'][i],shading='nearest',vmin=-80,vmax=0,cmap='viridis',rasterized=True);ax.set(xlabel='Time (s)',title=title,xticks=[0,2,4],yticks=[0,2,4,6,8]);ax.set_ylim(0,8)
axs[0].set_ylabel('Frequency (kHz)');cax=fig.add_axes([.925,.24,.013,.64]);cax.set_label('<colorbar>');cb=fig.colorbar(im,cax=cax);cb.set_label('Relative power (dB)',fontsize=7);save(fig,'failure_case',list(axs))
# Fig. 7: prespecified paired differences with cluster-bootstrap percentile CIs.
r=[z for z in read('primary_comparisons.csv') if z['Endpoint']=='EER' and z['SynchronousRegistration']=='0'];fig,ax=plt.subplots(figsize=(3.48,2.18));fig.subplots_adjust(left=.37,right=.98,bottom=.25,top=.94)
for j,z in enumerate(r):
 x=float(z['Difference_pp']);lo=float(z['Lower95_pp']);hi=float(z['Upper95_pp']);ax.errorbar(x,j,xerr=[[x-lo],[hi-x]],fmt='o',color='#2778ad' if j<2 else '#72983f',capsize=3,ms=4)
ax.axvline(0,c='#777777',lw=.8);ax.set(yticks=range(4),yticklabels=['SS 1.5 − Noisy','DFN − Noisy','SS 0.5 − SS 1.5','SS 0.5 − SS 3'],xlabel='EER difference (percentage points)',xlim=(-4.1,4.1),xticks=[-4,-2,0,2,4]);ax.invert_yaxis();save(fig,'bootstrap_analysis')
print('Seven report figures exported as vector PDFs (point clouds and spectrogram data rasterized only).')
