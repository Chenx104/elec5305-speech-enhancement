# MATLAB helper directory layout

The student-developed MATLAB implementation is inside the local-function appendix of `final_project.mlx`. The former separate `.m` copies are preserved in the external cleanup backup.

This directory is intentionally retained because the unchanged Python input initializer creates a historical `matlab` symlink to it. The merged Live Script resolves its MATLAB helper calls locally and does not load implementation functions from this directory. VOICEBOX remains a separately configured external dependency.

`clean_query/` contains standalone MATLAB helpers used only by `src/scripts/clean_query/reproduce.py` to repeat the small clean-query experiment. The main Live Script contains the same supplementary orchestration, DSP preparation, metric checks and display as local functions; its main execution does not need these separate helpers on the MATLAB path.
