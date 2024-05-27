"""Full TDE-HMM Burst Detection Pipeline.

Functions listed in the config are defined in osl_dynamics.config_api.wrappers.
"""

from sys import argv

if len(argv) != 4:
    print(
        "Please pass the channel index, number of states and run id, "
        "e.g. python run.py 3 0 1"
    )
    exit()
n_states = int(argv[1])
channel = int(argv[2])
id = int(argv[3])

import numpy as np
from glob import glob

from osl_dynamics.data import Data, processing
from osl_dynamics import run_pipeline


def load_single_channel_data():
    files = sorted(glob("data/npy/*.npy"))
    inputs = []
    for file in files:
        x = np.load(file)[:, channel]
        x = x[:, np.newaxis]
        x = processing.downsample(x, new_freq=100, old_freq=250)
        inputs.append(x)
    data = Data(
        inputs,
        sampling_frequency=100,
        store_dir=f"tmp_{n_states}_{channel}_{id}",
    )
    methods = {
        "tde": {"n_embeddings": 21},
        "standardize": {},
    }
    data.prepare(methods)
    return data


config = f"""
    train_hmm:
        config_kwargs:
            n_states: {n_states}
            learn_means: False
            learn_covariances: True
    multitaper_spectra:
        kwargs:
            frequency_range: [1, 45]
    plot_state_psds: {{}}
    plot_tde_covariances: {{}}
    plot_burst_summary_stats: {{}}
"""

run_pipeline(
    config,
    data=load_single_channel_data(),
    output_dir=f"results/{n_states}_states/channel{channel:03d}/run{id:02d}",
    extra_funcs=[load_single_channel_data],
)
