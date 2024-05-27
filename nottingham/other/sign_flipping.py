"""Standalone script for peforming sign flipping with npy data.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

import os
import numpy as np

from osl.source_recon.sign_flipping import (
    load_covariances,
    find_template_subject,
    find_flips,
    apply_flips,
)

# Settings
n_embeddings = 15
standardize = True
n_init = 2
n_iter = 2500
max_flips = 20

# Output directory
output_dir = "sign_flipped_data"
os.makedirs(output_dir, exist_ok=True)

# Input data
files = []
for i in range(1, 11):
    files.append(f"path/to/subject{i}.npy")

# Get covariance matrices
covs = load_covariances(
    files,
    n_embeddings,
    standardize,
    loader=np.load,
)

# Find a subject to use as a template
template = find_template_subject(covs, n_embeddings)
print("Using template:", files[template])

# Loop through each subject
for i in range(len(files)):
    print("Subject", i + 1)

    if i == template:
        # Don't need to do sign flipping on the template subject
        parc_data = np.load(files[i])
        np.save(f"{output_dir}/sflip{i + 1}.npy", parc_data)
        continue

    # Find the channels to flip
    flips, metrics = find_flips(
        covs[i], covs[template], n_embeddings, n_init, n_iter, max_flips
    )

    # Apply flips to the parcellated data and save
    parc_data = np.load(files[i])
    parc_data *= flips[np.newaxis, ...]
    np.save(f"{output_Dir}/sflip{i + 1}.npy", parc_data)
