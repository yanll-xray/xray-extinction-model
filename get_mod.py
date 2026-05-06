import os
import numpy as np
from heasp import *



file = "yllext.dat"
data = []
with open(file, "r") as f:
    for line in f:
        line = line.strip()

        if line.startswith("#") or len(line) == 0:
            continue

        parts = line.split()

        if len(parts) < 5:
            continue

        try:
            row = [float(x) for x in parts[:5]]
            data.append(row)
        except:
            pass

data = np.array(data)
E     = data[:,0] / 1e3   # eV -> keV
sigma = data[:,4]

E_low  = 0.01
E_high = 20.0
nE = 3000
E_ext = np.logspace(np.log10(E_low), np.log10(E_high), nE)


sigma_interp = np.interp(E_ext, E, sigma)
sigma_ext = np.zeros_like(E_ext)

E_min = E.min()
E_max = E.max()

mask_mid = (E_ext >= E_min) & (E_ext <= E_max)
sigma_ext[mask_mid] = sigma_interp[mask_mid]

mask_low = (E_ext < E_min)
sigma_ext[mask_low] = sigma[0] * (E_ext[mask_low] / E_min) ** (-3)

mask_high = (E_ext > E_max)
sigma_ext[mask_high] = sigma[-1] * (E_ext[mask_high] / E_max) ** (-3)


dE = np.diff(E_ext)
dE = np.append(dE, dE[-1])

E_edges = np.zeros(len(E_ext) + 1)
E_edges[1:-1] = 0.5 * (E_ext[:-1] + E_ext[1:])
E_edges[0] = E_ext[0] - dE[0] / 2
E_edges[-1] = E_ext[-1] + dE[-1] / 2
E_edges[E_edges < 0] = 1e-6


model = table()
model.setModelName("yllext")
model.setModelUnits("1")
model.setisRedshift(False)
model.setisAdditive(False)
model.setisError(False)

model.setEnergies(E_edges)

model.setNumIntParams(1)
model.setNumAddParams(0)

nh_grid = np.logspace(19, 23, 40)
nh_xspec = nh_grid / 1e22

p1 = tableParameter()
p1.setName("nH")
p1.setUnits("10^22")
p1.setInterpolationMethod(0)
p1.setInitialValue(0.1)
p1.setDelta(0.01)
p1.setMinimum(0.01)
p1.setBottom(0.01)
p1.setTop(10.0)
p1.setMaximum(10.0)
p1.setTabulatedValues(nh_xspec)

model.pushParameter(p1)


for nh in nh_xspec:

    tau = nh * 1e22 * sigma_ext
    flux = np.exp(-tau)

    spec = tableSpectrum()
    spec.setParameterValues(np.array([nh]))
    spec.setFlux(flux.astype(np.float32))

    model.pushSpectrum(spec)

outfile = "yllext.mod"

if os.path.exists(outfile):
    os.remove(outfile)

status = model.write(outfile)

if status != 0:
    print("ERROR:", status)
else:
    print("===========================================")
    print(" XSPEC physical model created:")
    print("   ", outfile)
    print("===========================================")
    print("XSPEC usage:")
    print(f" model mtable{{{outfile}}}*powerlaw")