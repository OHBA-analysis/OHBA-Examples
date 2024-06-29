"""Plot networks.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

import os
import numpy as np

from osl_dynamics.analysis import power, connectivity
from osl_dynamics.utils import plotting

subject = "LN_VTA2"

# Output directory
os.makedirs(f"hmm/{subject}/plots", exist_ok=True)

# Load multitaper spectra
f = np.load(f"hmm/{subject}/f.npy")
psd = np.load(f"hmm/{subject}/psd.npy")
coh = np.load(f"hmm/{subject}/coh.npy")

# Plot PSDs
p = np.mean(psd, axis=1)
for i in range(p.shape[0]):
    plotting.plot_line(
        [f],
        [p[i]],
        x_label="Frequency (Hz)",
        y_label="PSD (a.u.)",
        x_range=[f[0], f[-1]],
        filename=f"hmm/{subject}/plots/psd_{i:02d}.png",
    )

# Plot power maps
pow_maps = power.variance_from_spectra(f, psd)

power.save(
    pow_maps,
    subtract_mean=True,
    mask_file="MNI152_T1_8mm_brain.nii.gz",
    parcellation_file="Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
    plot_kwargs={"symmetric_cbar": True},
    filename=f"hmm/{subject}/plots/pow_.png",
)

# Plot coherence networks
coh_nets = connectivity.mean_coherence_from_spectra(f, coh)
coh_nets -= np.mean(coh_nets, axis=0)
coh_nets = connectivity.threshold(coh_nets, percentile=97, absolute_value=True)

connectivity.save(
    coh_nets,
    parcellation_file="Glasser52_binary_space-MNI152NLin6_res-8x8x8.nii.gz",
    filename=f"hmm/{subject}/plots/coh_.png",
)
