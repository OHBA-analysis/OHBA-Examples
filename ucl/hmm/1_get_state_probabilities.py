"""Infer state probabilities by applying the normative model to a dataset.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

import os
import mne
import numpy as np
from scipy import io

from osl_dynamics.data import Data
from osl_dynamics.models import load
from osl_dynamics.inference import modes

subject = "LN_VTA2"

# Load sign flipped data
data = Data(f"../preproc/data/npy/{subject}.npy")

# Prepare data
pca_components = np.load("../camcan_norm_model/pca_components.npy")
data.prepare({
    "tde_pca": {"n_embeddings": 15, "pca_components": pca_components},
    "standardize": {},
})

# Load model
model = load("../camcan_norm_model")

# Get state probabilities
alpha = model.get_alpha(data)

# Make output directory
os.makedirs(f"hmm/{subject}", exist_ok=True)

# Save in python format
#np.save(f"hmm/{subject}/alpha.npy", alpha)

# Convert to MNE raw object
source_raw = mne.io.read_raw_fif(
    f"../preproc/data/src/{subject}/parc/parc-raw.fif",
    verbose=False,
)  # note: this is not sign flipped
alpha_raw = modes.convert_to_mne_raw(alpha, source_raw, n_embeddings=15)

# Get data (including bad segments as 0 values)
X = source_raw.get_data(picks="misc")
P = alpha_raw.get_data()
X = {"X": X, "P": P}

# Save in Matlab format
io.savemat(f"hmm/{subject}/X.mat", X)

# Delete temporary directory
data.delete_dir()
