# Human Connectome Project (HCP)

Start-to-end example scripts for training a Hidden Markov Model (HMM) on HCP resting-state fMRI data.

Download the dataset from [here](https://db.humanconnectome.org/data/projects/HCP_1200). You will need to create an account to download the data.

Download the following dataset:
```
HCP1200 Parcellation+Timeseries+Netmats (PTN)
1003 Subjects, recon r177 + r227, PTN Release (13GB)
```

This contains fMRI data with independent component analysis (ICA) applied.

We will train an HMM on the ICA time courses. This is the recommended approach for studying fMRI data with an HMM, see this [paper](https://www.sciencedirect.com/science/article/pii/S1053811922001550). In this example, we will study the 25 component ICA.

The ICA parcellations are in: `groupICA_3T_HCP1200_MSMAll.tar.gz`. Specifically:
```
groupICA/groupICA_3T_HCP1200_MSMAll_d25.ica/melodic_IC.dscalar.nii
```

The node time series are in: `NodeTimeseries_3T_HCP1200_MSMAll_ICAd25_ts2.tar.gz`. Specifically:
```
node_timeseries/3T_HCP1200_MSMAll_d25_ts2/*.txt
```
