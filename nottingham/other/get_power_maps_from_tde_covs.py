"""Get state power maps directly from inferred state covariances
trained on time-delay embedded (TDE) data.

"""

import numpy as np

from osl_dynamics.data import Data
from osl_dynamics.analysis import modes

# Load data
#
# Note, we need to prepare it in the same way we did when
# training the model
data = Data("data/npy", n_jobs=16)
methods = {
    "tde_pca": {"n_embeddings": 15, "n_pca_components": 140},
    "standardize": {},
}
data.prepare(methods)

# Load inferred covariances in TDE space
covs = np.load(f"results/8_states/run01/inf_params/covs.npy")

print("TDE covariances shape:", covs.shape)

# Calculate covariances in pre-preparation space
# In our case the data was in parcel space
covs = modes.raw_covariances(
    covs,
    n_embeddings=data.n_embeddings,
    pca_components=data.pca_components,
)

print("Parcel covariances shape:", covs.shape)

# Power maps are the diagonal of each covariance matrix
power_maps = np.diagonal(covs, axis1=1, axis=2)

print("Power maps shape:", power_maps.shape)

# Can be saved with:
#np.save("power_maps.npy", power_maps)
