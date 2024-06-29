"""Calculate multitaper spectra.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

import os
import numpy as np

from osl_dynamics.data import Data
from osl_dynamics.analysis import spectral

subject = "LN_VTA2"

# Load source data
data = Data(f"../preproc/data/npy/{subject}.npy")
x = data.trim_time_series(n_embeddings=15, sequence_length=2000)

# Load state probabilities
alpha = np.load(f"hmm/{subject}/alpha.npy")

# Calculate multitaper
f, psd, coh = spectral.multitaper_spectra(
    data=x,
    alpha=alpha,
    sampling_frequency=250,
    frequency_range=[1, 45],
)

# Save
os.makedirs(f"hmm/{subject}", exist_ok=True)
np.save(f"hmm/{subject}/f.npy", f)
np.save(f"hmm/{subject}/psd.npy", psd)
np.save(f"hmm/{subject}/coh.npy", coh)

# Delete temporary directory
data.delete_dir()
