# MATLAB helper directory layout

The student-developed MATLAB implementation is inside the local-function appendix of `final_project.mlx`. The former separate `.m` copies are preserved in the external cleanup backup.

This directory is intentionally retained because the unchanged Python input initializer creates a historical `matlab` symlink to it. The merged Live Script resolves its MATLAB helper calls locally and does not load implementation functions from this directory. VOICEBOX remains a separately configured external dependency.
