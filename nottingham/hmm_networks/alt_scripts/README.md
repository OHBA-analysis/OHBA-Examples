# TDE-HMM Network Analysis Using Low-Level Functions

In this example we call the underlying osl-dynamics functions directly:

- `1_train_hmm.py`: Train a TDE-HMM. We pass the number of states and a run ID to this script, e.g. `python 1_train_hmm.py 8 1`, where `8` is the number of states and `1` is the run ID. You generally want to train multiple HMMs (with different run IDs) and pick the best (lowest free energy) run.
- `2_print_free_energy.py`: This prints the free energy for each HMM run.
- `3_get_inf_params.py`: Get the inferred state probabilities, means and covariances. Note, with the TDE-HMM approach we set the state means to zero.
- `4_calc_multitaper.py`: Post-hoc calculation of subject and state-specific power/coherence spectra using a multitaper.
- `5_plot_networks.py`: Plot the group-average networks from the multitaper.
- `6_calc_summary_stats.py`: Calculate and plot the distribution of summary statistics for dynamics (fractional occupancy, lifetime, interval, switching rate) across subjects.

Note, there is a variable called `n_jobs` in these scripts that should be set to the number of cores you would like to use.
