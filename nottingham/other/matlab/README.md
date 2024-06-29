# uk-meg-notts

Scripts to fit an HMM to the uk_meg_notts dataset using Matlab.

Repos:

- MATLAB OSL: https://ohba-analysis.github.io/osl-docs (now obsolete)
- HMM-MAR: https://github.com/OHBA-analysis/HMM-MAR

Full pipeline:
```
matlab
>> osl_startup;
>> convert_raw_data;
>> preprocess_data;
>> source_reconstruct;
>> prepare_te_pca_data;
>> fit_hmm;
>> analyse_hmm_fit;
>> save_maps;
```
