import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from deepQTrading import DeepQTrading
import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, LeakyReLU
from tensorflow.keras.optimizers import Adam

# Libraries used for the Agent considered
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy

import sys
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto, Session
from tensorflow.compat.v1.keras.backend import set_session

# Set TensorFlow GPU memory limit
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
session = Session(config=config)
set_session(session)

# Parse command-line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--nb_actions', type=int, required=True, help='Number of actions')
parser.add_argument('--is_only_short', type=int, required=True, help='1 if only short, 0 otherwise')
parser.add_argument('--ensemble_folder', type=str, required=True, help='Folder name for ensemble results')

args = parser.parse_args()
nb_actions = args.nb_actions
isOnlyShort = args.is_only_short == 1
ensembleFolderName = args.ensemble_folder

# Model setup
model = Sequential()
model.add(Flatten(input_shape=(1, 1, 68)))
model.add(Dense(35, activation='linear'))
model.add(LeakyReLU(alpha=.001))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

# Ensure output directory exists
output_dir = "./Output/csv/walks/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Deep Q-Trading initialization
dqt = DeepQTrading(
    model=model,
    explorations=[(0.2, 100)],
    trainSize=datetime.timedelta(days=360 * 5),
    validationSize=datetime.timedelta(days=30 * 6),
    testSize=datetime.timedelta(days=30 * 6),
    outputFile=os.path.join(output_dir, "walks"),
    begin=datetime.datetime(2001, 1, 1, 0, 0, 0, 0),
    end=datetime.datetime(2019, 2, 28, 0, 0, 0, 0),
    nbActions=nb_actions,
    isOnlyShort=isOnlyShort,
    ensembleFolderName=ensembleFolderName
)

# Run the trading agent
dqt.run()

# End the agent process
dqt.end()
