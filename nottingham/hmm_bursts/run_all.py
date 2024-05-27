"""Train a series of HMMs.

"""

import os

n_states = 3
run_id = 1
n_channels = 78

for channel_index in range(n_channels):
    cmd = f"python run.py {n_states} {channel_index} {run_id}"
    print(cmd)
    os.system(cmd)
