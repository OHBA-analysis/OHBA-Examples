# Example scripts for fitting a pretrained HMM

In this example we:

- `1_get_state_probabilities.py`: Use the CamCAN (rest and task) normative model to estimate the probabilities of each state being active at each time point for a given subject.
- `2_calc_summary_stats.py`: Calculate summary statistics from the state probabilities.
- `3_calc_multitaper.py`: Calculate post-hoc spectra using a multitaper.
- `4_plot_networks.py`: Plot networks from the multitaper spectra.
