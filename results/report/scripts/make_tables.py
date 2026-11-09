from pathlib import Path
import csv
D=Path(__file__).resolve().parents[1];S=D/'source_data';T=D/'tables';T.mkdir(exist_ok=True);read=lambda n:list(csv.DictReader((S/n).open()));r={x['Method']:x for x in read('overall_results.csv')}
methods=['Noisy','SS_a0p5','SS_a1p0','SS_a1p5','SS_a2p0','SS_a3p0','VAD_SS','Tracking_SS','DeepFilterNet'];names=['Noisy','SS $\\alpha=0.5$ (EER-selected)','SS $\\alpha=1$','SS $\\alpha=1.5$ (default)','SS $\\alpha=2$','SS $\\alpha=3$ (SI-SDR-selected)','VAD-SS','Tracking-SS','DeepFilterNet3']
lines=[r'\begin{tabular}{lrrrrrrr}',r'\toprule',r'Method & SI-SDR (dB) & Gain (dB) & STOI & $\Delta$STOI & EER (\%) & BER (\%) & $\dcos$\\',r'\midrule']
for m,n in zip(methods,names):
 x=r[m];v=[float(x[k]) for k in ['SI_SDR_dB','TargetSI_SDRGain_dB','STOI','TargetSTOIChange','ExternalEER_pct','CommonThresholdBER_pct','MeanDeltaCos']];lines.append(n+' & '+' & '.join([f'{v[0]:.3f}',f'{v[1]:.3f}',f'{v[2]:.4f}',f'{v[3]:+.4f}' if abs(v[3])>1e-7 else '0.0000',f'{v[4]:.3f}',f'{v[5]:.3f}',f'{v[6]:+.4f}' if abs(v[6])>1e-8 else '0.0000'])+r'\\')
lines += [r'\bottomrule',r'\end{tabular}'];(T/'overall_rows.tex').write_text('\n'.join(lines)+'\n')
r=[x for x in read('robustness_summary.csv') if x['Endpoint']=='EER'];names=['SS 1.5 $-$ Noisy','DFN $-$ Noisy','SS 0.5 $-$ SS 1.5','SS 0.5 $-$ SS 3'];lines=[r'\begin{tabular}{lrr}',r'\toprule',r'Comparison & Alternative & Source-omission\\',r' & enrollment & range\\',r'\midrule']
for x,n in zip(r,names):lines.append(n+f" & {float(x['AlternativeEnrollmentDifference_pp']):+.3f} & [{float(x['LeaveSourceMinimum_pp']):+.3f}, {float(x['LeaveSourceMaximum_pp']):+.3f}]"+r'\\')
lines += [r'\bottomrule',r'\end{tabular}'];(T/'robustness_rows.tex').write_text('\n'.join(lines)+'\n');print('Tables generated directly from verified CSVs.')
