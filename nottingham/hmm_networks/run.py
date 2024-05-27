"""Full TDE-HMM Network Analysis Pipeline.

Functions listed in the config are defined in osl_dynamics.config_api.wrappers.

Note, the recommended number of PCA components is approximately twice the
number of original parcels.
"""

from sys import argv

if len(argv) != 3:
    print("Please pass the number of states and run id, e.g. python run.py 8 1")
    exit()
n_states = int(argv[1])
id = int(argv[2])

from osl_dynamics import run_pipeline

config = f"""
    load_data:
        inputs: data/npy
        kwargs:
            sampling_frequency: 250
            mask_file: ft_8mm_brain_mask.nii.gz
            parcellation_file: aal_cortical_merged_8mm_stacked.nii.gz
            n_jobs: 16
        prepare:
            tde_pca: {{n_embeddings: 15, n_pca_components: 140}}
            standardize: {{}}
    train_hmm:
        config_kwargs:
            n_states: {n_states}
            learn_means: False
            learn_covariances: True
            sequence_length: 1000
    multitaper_spectra:
        kwargs:
            frequency_range: [1, 45]
            n_jobs: 16
        nnmf_components: 2
    plot_group_nnmf_tde_hmm_networks:
        nnmf_file: spectra/nnmf_2.npy
        power_save_kwargs:
            plot_kwargs: {{views: [lateral], symmetric_cbar: True}}
    plot_alpha:
        kwargs: {{n_samples: 2000}}
    plot_hmm_network_summary_stats:
        sns_kwargs: {{cut: 0}}
"""

run_pipeline(config, output_dir=f"results/{n_states}_states/run{id:02d}")
