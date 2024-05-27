"""Get inferred parameters (state probabilities, means, covariances).

"""

from sys import argv

if len(argv) != 3:
    print("Please pass the number of states and run id, e.g. python 3_get_inf_params.py 8 1")
    exit()
n_states = int(argv[1])
run = int(argv[2])

#%% Import packages

print("Importing packages")

import os
import pickle
import numpy as np

from osl_dynamics.data import Data
from osl_dynamics.models import load

#%% Setup directories

# Directories
model_dir = f"results/{n_states}_states/run{run:02d}/model"
inf_params_dir = f"results/{n_states}_states/run{run:02d}/inf_params"

os.makedirs(inf_params_dir, exist_ok=True)

#%% Prepare data

# Load data
data = Data(
    "data/npy",
    store_dir=f"tmp_{n_states}_{run}",
    use_tfrecord=True,
    n_jobs=16,
)

# Perform time-delay embedding and PCA
methods = {
    "tde_pca": {"n_embeddings": 15, "n_pca_components": 140},
    "standardize": {},
}
data.prepare(methods)

#%% Load model

model = load(model_dir)

#%% Get inferred parameters

# State probabilities
alp = model.get_alpha(data)

pickle.dump(alp, open(f"{inf_params_dir}/alp.pkl", "wb"))

# Observation model parameters
means, covs = model.get_means_covariances()

np.save(f"{inf_params_dir}/means.npy", means)
np.save(f"{inf_params_dir}/covs.npy", covs)

#%% Delete temporary directory

data.delete_dir()

