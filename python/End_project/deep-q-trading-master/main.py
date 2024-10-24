import os
import argparse
import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, LeakyReLU
from tensorflow.keras.optimizers import Adam

# Keras-RL2 imports (install with `pip install keras-rl2`)
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--nb_actions', type=int, required=True, help='Number of actions')
parser.add_argument('--is_only_short', type=int, required=True, help='1 if only short, 0 otherwise')
parser.add_argument('--ensemble_folder', type=str, required=True, help='Folder name for ensemble results')

args = parser.parse_args()
nb_actions = args.nb_actions
isOnlyShort = args.is_only_short == 1
ensembleFolderName = args.ensemble_folder

# TensorFlow 2.x config for GPU memory limiting
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.experimental.set_virtual_device_configuration(gpu, [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3072)]) # Memory limit example: 3GB
    except RuntimeError as e:
        print(e)

# Model setup
model = Sequential()
model.add(Flatten(input_shape=(1, 1, 68)))
model.add(Dense(35, activation='linear'))
model.add(LeakyReLU(alpha=0.001))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

# Ensure output directory exists
output_dir = "./Output/csv/walks/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Deep Q-Trading initialization (assuming deepQTrading is a custom library)
dqt = DeepQTrading(
    model=model,
    explorations=[(0.2, 100)],  # Exploration schedule
    trainSize=datetime.timedelta(days=360 * 5),
    validationSize=datetime.timedelta(days=30 * 6),
    testSize=datetime.timedelta(days=30 * 6),
    outputFile=os.path.join(output_dir, "walks"),
    begin=datetime.datetime(2001, 1, 1),
    end=datetime.datetime(2019, 2, 28),
    nbActions=nb_actions,
    isOnlyShort=isOnlyShort,
    ensembleFolderName=ensembleFolderName
)

# Run the trading agent
dqt.run()

# End the agent process
dqt.end()
