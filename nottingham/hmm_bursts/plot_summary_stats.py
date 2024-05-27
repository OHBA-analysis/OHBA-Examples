"""Plots results for a particular run.

"""

import numpy as np

from osl_dynamics.analysis import power
from osl_dynamics.utils import plotting

n_states = 3
run_id = 1
n_channels = 78

def get_beta_state(channel):
    results_dir = f"results/{n_states}_states/channel{channel:03d}/run{run_id:02d}"
    f = np.load(f"{results_dir}/spectra/f.npy")
    psd = np.load(f"{results_dir}/spectra/psd.npy")
    gpsd = np.mean(psd, axis=0)
    p = power.variance_from_spectra(f, gpsd, frequency_range=[13, 30])
    return np.argmax(p)

def get_summary_stats(channel):
    results_dir = f"results/{n_states}_states/channel{channel:03d}/run{run_id:02d}"
    lt = np.load(f"{results_dir}/summary_stats/lt.npy")
    bc = np.load(f"{results_dir}/summary_stats/bc.npy")
    amp = np.load(f"{results_dir}/summary_stats/amp.npy")
    intv = np.load(f"{results_dir}/summary_stats/intv.npy")
    return lt, bc, amp, intv


# Load summary statistics for each channel
lifetime = []
burst_count = []
amplitude = []
interval = []
for channel in range(n_channels):
    beta_state = get_beta_state(channel)
    lt, bc, amp, intv = get_summary_stats(channel)
    lifetime.append(lt[:, beta_state])   # s
    burst_count.append(bc[:, beta_state])  # Hz
    amplitude.append(amp[:, beta_state])  # a.u.
    interval.append(intv[:, beta_state])  # s

# Average over subjects
lifetime = np.mean(lifetime, axis=-1)
burst_count = np.mean(burst_count, axis=-1)
amplitude = np.mean(amplitude, axis=-1)
interval = np.mean(interval, axis=-1)

# Plot
plotting.plot_brain_surface(
    lifetime,
    mask_file="ft_8mm_brain_mask.nii.gz",
    parcellation_file="aal_cortical_merged_8mm_stacked.nii.gz",
    plot_kwargs={"cmap": "jet", "vmin": lifetime.min(), "vmax": lifetime.max()},
    filename="lifetime_.png",
)
plotting.plot_brain_surface(
    burst_count,
    mask_file="ft_8mm_brain_mask.nii.gz",
    parcellation_file="aal_cortical_merged_8mm_stacked.nii.gz",
    plot_kwargs={"cmap": "jet", "vmin": burst_count.min(), "vmax": burst_count.max()},
    filename="burst_count_.png",
)
plotting.plot_brain_surface(
    amplitude,
    mask_file="ft_8mm_brain_mask.nii.gz",
    parcellation_file="aal_cortical_merged_8mm_stacked.nii.gz",
    plot_kwargs={"cmap": "jet", "vmin": amplitude.min(), "vmax": amplitude.max()},
    filename="amplitude_.png",
)
plotting.plot_brain_surface(
    interval,
    mask_file="ft_8mm_brain_mask.nii.gz",
    parcellation_file="aal_cortical_merged_8mm_stacked.nii.gz",
    plot_kwargs={"cmap": "jet", "vmin": interval.min(), "vmax": interval.max()},
    filename="interval_.png",
)
