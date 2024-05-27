"""Train an HMM on time-delay embedded/PCA data.

You want to train multiple HMMs and just analyse the one with the lowest
free energy. Historically, picking the best of 10 runs has worked well.
"""

from sys import argv

if len(argv) != 3:
    print("Please pass the number of states and run id, e.g. python 1_train_hmm.py 8 1")
    exit()
n_states = int(argv[1])
run = int(argv[2])

#%% Import packages

print("Importing packages")

import pickle

from osl_dynamics.data import Data
from osl_dynamics.models.hmm import Config, Model

#%% Load data

# Load data
data = Data(
    "data/npy",
    store_dir=f"tmp_{n_states}_{run}",
    use_tfrecord=True,
    n_jobs=16,
)

# Prepare data
#
# Note:
# - We recommend approximately twice the number of original channels
#   for the number of PCA components.
# - We find 15 embeddings works well for inferring dynamic networks.
methods = {
    "tde_pca": {"n_embeddings": 15, "n_pca_components": 140},
    "standardize": {},
}
data.prepare(methods)

#%% Setup model

# Settings
config = Config(
    n_states=n_states,
    n_channels=data.n_channels,
    sequence_length=1000,
    learn_means=False,
    learn_covariances=True,
    batch_size=32,
    learning_rate=0.01,
    n_epochs=20,
)

# Note:
# - The training time will depend on the sequence_length and batch_size
#   you may want to play around with these to reduce the training time on
#   your specific computer.
# - You may not need to do 20 epochs to train your model. You may find the
#   loss has converged in the first few epochs.

# Create model
model = Model(config)
model.summary()

#%% Training

# Initialisation
init_history = model.random_state_time_course_initialization(data, n_init=3, n_epochs=1)

# Full training
history = model.fit(data)

# Save trained model
model_dir = f"results/{n_states}_states/run{run:02d}/model"
model.save(model_dir)

# Calculate the free energy
free_energy = model.free_energy(data)
history["free_energy"] = free_energy

# Save training history and free energy
pickle.dump(init_history, open(f"{model_dir}/init_history.pkl", "wb"))
pickle.dump(history, open(f"{model_dir}/history.pkl", "wb"))

#%% Delete temporary directory

data.delete_dir()
