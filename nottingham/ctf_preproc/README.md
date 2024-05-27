# CTF Data Example

Preprocessing and source reconstruction of CTF data.

## Dataset

We use the public CTF data from the Nottingham in the MEGUK Partnership dataset: [https://meguk.ac.uk/database/](https://meguk.ac.uk/database/).

We use the resting-state (eyes open) data. These example scripts expect the data to be in the original directory structure in the public dataset:

```
data
|-- raw
    |-- Nottingham
        |-- sub-not001
            |-- meg
                |-- sub-not001_task-resteyesopen_meg.ds
                |-- ...
            |-- anat
                |-- sub-not001_T1w.nii.gz
                |-- ...
        |-- sub-not002
        |-- ...
```

## Structural MRIs

Note, there is an incompatibility with the structural MRIs (sMRIs) in the public MEGUK dataset and OSL. The issue is OSL can only use sMRI files that have a certain sform code. We can easily fix the sMRI files by just changing the sform code. An example script for doing this is in `../other/fix_smri_files.py`.

## Pipeline

In this example we:

- `1_preprocess.py`: Preprocess the sensor-level data. This includes standard signal processing such as downsampling and filtering as well as artefact removal.
- `2_coregister.py`: Coregister the MEG and sMRI data and calculate the forward model.
- `3_source_reconstruct.py`: Beamform the sensor-level data and parcellate to give us the source-level data. We use the AAL parcellation.
- `4_sign_flip.py`: Fix the dipole sign ambiguity (we align the sign of the parcel time courses across subjects). This is only needed if we're training a group-level model on time-delay emebdded data.
- `5_save_npy.py`: Save the source data as vanilla numpy files in (time, parcels) format.

## Parallelisation

See [here](https://github.com/OHBA-analysis/osl/tree/main/examples/parallelisation) for how to parallelise these scripts.
