# Likelihood fits for the advanced physics laboratory courses at the KIT

This repository provides the python scripts used in the bachelor thesis
*Likelihood fits for the advanced physics laboratory courses at the KIT*.

The Bachelor Thesis focuses on implementing Unbinned Likelihood-Fits in the software tool
[kafe2](https://github.com/dsavoiu/kafe2).
This fitting method and the Binned Likelihood-Fits are used in conjunction with the Multifit in kafe2 for analysing
data from the physics laboratory course
*determing the Landé-factor of the myon*.



## Getting started
The fits are done with the pre-release version `0.1.0` of `kafe2`.
This version is included as a git submodule in this repository. Please download it and run `pip install .` when inside the kafe2 directory.

Most of the scripts require the `iminuit` minimizer to be installed. This minimizer isn't installed with `kafe`.
Please run `pip install iminuit` before running the scripts.
