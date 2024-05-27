"""Calculate summary statistics.

"""

from sys import argv

if len(argv) != 3:
    print("Please pass the number of states and run id, e.g. python 6_calc_summary_stats.py 8 1")
    exit()
n_states = int(argv[1])
run = int(argv[2])

#%% Import packages

print("Importing packages")

import os
import pickle
import numpy as np

from osl_dynamics.inference import modes
from osl_dynamics.utils import plotting

#%% Setup directories

# Directories
inf_params_dir = f"results/{n_states}_states/run{run:02d}/inf_params"
summary_stats_dir = f"results/{n_states}_states/run{run:02d}/summary_stats"

os.makedirs(summary_stats_dir, exist_ok=True)

#%% Load state time course

# State probabilities
alp = pickle.load(open(f"{inf_params_dir}/alp.pkl", "rb"))

# Calculate a state time course by taking the most likely state
stc = modes.argmax_time_courses(alp)

#%% Calculate summary statistics

print("Calculating summary stats")

# Fractional occupancy
fo = modes.fractional_occupancies(stc)

# Mean lifetime
lt = modes.mean_lifetimes(stc, sampling_frequency=250)

# Mean interval
intv = modes.mean_intervals(stc, sampling_frequency=250)

# Mean switching rate
sr = modes.switching_rates(stc, sampling_frequency=250)

# Save
np.save(f"{summary_stats_dir}/fo.npy", fo)
np.save(f"{summary_stats_dir}/lt.npy", lt)
np.save(f"{summary_stats_dir}/intv.npy", intv)
np.save(f"{summary_stats_dir}/sr.npy", sr)

# Plot
n_states = fo.shape[1]
x = range(1, n_states + 1)
plotting.plot_violin(
    fo.T,
    x=x,
    x_label="State",
    y_label="Fractional Occupancy",
    filename=f"{summary_stats_dir}/fo.png",
    sns_kwargs={"cut": 0},
)
plotting.plot_violin(
    lt.T,
    x=x,
    x_label="State",
    y_label="Mean Lifetime (s)",
    filename=f"{summary_stats_dir}/lt.png",
    sns_kwargs={"cut": 0},
)
plotting.plot_violin(
    intv.T,
    x=x,
    x_label="State",
    y_label="Mean Interval (s)",
    filename=f"{summary_stats_dir}/intv.png",
    sns_kwargs={"cut": 0},
)
plotting.plot_violin(
    sr.T,
    x=x,
    x_label="State",
    y_label="Switching rate (Hz)",
    filename=f"{summary_stats_dir}/sr.png",
    sns_kwargs={"cut": 0},
)
