"""Recompute this small supplement only; keep original main-run results read-only."""
from pathlib import Path
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--python',required=True);p.add_argument('--matlab',default='/Applications/MATLAB_R2025b.app/bin/matlab');a=p.parse_args();here=Path(__file__).resolve().parent;matlab_helpers=here.parents[1]/'matlab'/'clean_query'
def run(cmd):subprocess.run([str(x)for x in cmd],check=True)
def matlab(function):
 q=lambda s:str(s).replace("'","''")
 run([a.matlab,'-batch',f"addpath('{q(matlab_helpers)}'); {function}('{q(a.output.resolve())}')"])
run([a.python,here/'prepare_supplement.py','--project',a.project,'--run',a.run,'--output',a.output])
matlab('prepare_clean_ss')
run([a.python,a.output/'scripts/run_deepfilter.py',a.output])
run([a.python,a.output/'scripts/extract_embeddings.py',a.output])
run([a.python,here/'analyze_clean.py','--root',a.output])
matlab('check_matlab_metrics')
