"""Perform dipole sign flipping.

"""

# Authors: Chetan Gohil <chetan.gohil@psych.ox.ac.uk>

from glob import glob
from dask.distributed import Client

from osl import source_recon, utils

src_dir = "/well/woolrich/projects/mrc_meguk/all_sites/src"
sflip_dir = "/well/woolrich/projects/mrc_meguk/all_sites/sflip"

if __name__ == "__main__":
    utils.logger.set_up(level="INFO")
    client = Client(n_workers=16, threads_per_worker=1)

    # Copy the parc-raw.fif files into one big directory
    for path in sorted(glob(f"{src_dir}/*/*/parc/parc-raw.fif")):
        subject = path.split("/")[-3]
        source_recon.rhino.utils.system_call(f"mkdir -p {sflip_dir}/{subject}/parc", verbose=True)
        source_recon.rhino.utils.system_call(f"cp {path} {sflip_dir}/{subject}/parc", verbose=True)

    subjects = []
    for path in sorted(glob(f"{sflip_dir}/*/parc/parc-raw.fif")):
        subject = path.split("/")[-3]
        subjects.append(subject)

    template = source_recon.find_template_subject(
        sflip_dir, subjects, n_embeddings=15, standardize=True
    )

    config = f"""
        source_recon:
        - fix_sign_ambiguity:
            template: {template}
            n_embeddings: 15
            standardize: True
            n_init: 3
            n_iter: 2500
            max_flips: 20
    """

    source_recon.run_src_batch(
        config,
        src_dir=sflip_dir,
        subjects=subjects,
        dask_client=True,
    )
