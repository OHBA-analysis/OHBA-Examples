"""Calculate summary stats.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

import os
import numpy as np

from osl_dynamics.inference import modes

subject = "LN_VTA2"

# Load state probabilities
alpha = np.load(f"hmm/{subject}/alpha.npy")

# Get state time course (Viterbi path)
stc = modes.argmax_time_courses(alpha)

# Calculate summary stats
fo = modes.fractional_occupancies(stc)
lt = modes.mean_lifetimes(stc)
intv = modes.mean_intervals(stc)
sr = modes.switching_rates(stc)

# Save
np.save(f"hmm/{subject}/fo.npy", fo)
np.save(f"hmm/{subject}/lt.npy", lt)
np.save(f"hmm/{subject}/intv.npy", intv)
np.save(f"hmm/{subject}/sr.npy", sr)
