# Likelihood fits for the advanced physics laboratory courses at the KIT

[![DOI](https://zenodo.org/badge/222707230.svg)](https://zenodo.org/badge/latestdoi/222707230)

This repository provides the python scripts used in the bachelor thesis
*Likelihood fits for the advanced physics laboratory courses at the KIT*.

The Bachelor Thesis focuses on implementing Unbinned Likelihood-Fits in the software tool
[kafe2](https://github.com/dsavoiu/kafe2).
This fitting method and the Binned Likelihood-Fits are used in conjunction with the multifit in kafe2 for analysing
data from the physics laboratory course
*determining the Landé-factor of the myon*.



## Getting started
The fits are done with the kafe2 version supplied as a git submodule.
Please run `git submodule init` and `git submodule update` in order to run the scripts.
This will initialize and download the kafe2 version the scripts were built and tested against.
The scripts will use the locally supplied kafe2 version. There is no need to install kafe2 system wide.

Most of the scripts require the iminuit minimizer to be installed.
Please run `pip install iminuit` before running the scripts.
