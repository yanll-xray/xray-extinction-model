# 1. Overview
This repository provides an interstellar X-ray extinction model
(Yan et al. 2026, ApJ, xxx, xxx; DOI: xxxxxxxx).

This model presents the energy-dependent X-ray extinction in the interstellar medium, 
including gas absorption, dust absorption, and dust scattering, by utilizing the latest 
interstellar abundances of heavy elements, and the updated dust physics. 
The elements locked up in dust grains were derived from reproducing the interstellar 
extinction from the far ultraviolet and near infrared. The model results are 
implemented as an XSPEC multiplicative table model.

# 2. Repository Contents
- yllext.dat  Energy-dependent cross sections (Fig. 3, Yan et al. 2026)
- get_mod.py  Python script to generate XSPEC table model
- yllext.mod  XSPEC model file
- example.xcm XSPEC fitting example

# 3. Requirements
yllext.mod was developed and tested using the following software environment:
- XSPEC 12.15.1 (HEASOFT 6.36)
- Python 3.10

Before running XSPEC or the model generation script, initialize HEASOFT:
> source $HEADAS/headas-init.sh

# 4. Generate Model
Run the following script to generate the XSPEC table model:
> python3 get_mod.py

Output: yllext.mod

# 5. XSPEC Usage
> XSPEC12> model mtable{yllext.mod}*powerlaw

Parameters:
- N_H (10^22 cm^-2)
- Photon index
- Normalization (photons keV^-1 cm^-2 s^-1)

# 6. Example Fit
Start XSPEC and run full fitting pipeline

> XSPEC12> @example.xcm

This script will:
- Load NICER Crab pulsar spectrum
- Apply yllext model
- Fit absorbed powerlaw model
- Generate residual plots
- Save PS output

# 7. Citation
L.L. Yan, A. Li, & F.J. Lu (2026), ApJ, xxx, xxx 

Contact: Linli Yan (yan.linli@foxmail.com) or Aigen Li (LiA@missouri.edu)

