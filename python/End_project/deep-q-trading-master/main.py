# Copyright (C) 2020 Salvatore Carta, Anselmo Ferreira, Alessandro Sebastian Podda,
# Diego Reforgiato Recupero, Antonio Sanna. All rights reserved.

# os library is used to define the GPU to be used by the code, needed only in cerain situations 
# (Better not to use it, use only if the main GPU is busy)
# import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# This is the class call for the Agent which will perform the experiment
from deepQTrading import DeepQTrading

# Date library to manipulate time in the source code
import datetime

# TensorFlow library to define the NN to be used
import tensorflow as tf
from tensorflow.keras.models import Sequential
# Layers used in the NN considered
from tensorflow.keras.layers import Dense, Activation, Flatten
# Activation Layers used in the source code
from tensorflow.keras.layers import LeakyReLU, PReLU, ReLU
# Optimizer used in the NN
from keras.optimizers import Adam

# Libraries used for the Agent considered
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy

# Library used for showing the exception in case of an error
import sys

# TensorFlow GPU memory configuration (optional)
# gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.3)
# session = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
# tf.compat.v1.keras.backend.set_session(session)

# Let's capture the starting time and send it to the destination in order to tell that the experiment started 
startingTime = datetime.datetime.now()

# There are three actions possible in the stock market
# Hold (id 0): do nothing.
# Long (id 1): It predicts that the stock market value will raise at the end of the day. 
# So, the action performed in this case is buying at the beginning of the day and selling it at the end of the day (aka long).
# Short (id 2): It predicts that the stock market value will decrease at the end of the day.
# So, the action that must be done is selling at the beginning of the day and buying it at the end of the day (aka short).
nb_actions = int(sys.argv[1])

isOnlyShort = sys.argv[2] == '1'

# This is a simple NN considered. It is composed of:
# One flatten layer to get 68 dimensional vectors as input
# One dense layer with 35 neurons and LeakyReLU activation
# One final Dense Layer with the 3 actions considered
# The input is 20 observation days from the past, 8 observations from the past week, and 
# 40 observations from the past hours
model = Sequential()
model.add(Flatten(input_shape=(1, 1, 68)))
model.add(Dense(35, activation='linear'))
model.add(LeakyReLU(alpha=0.001))
model.add(Dense(nb_actions))
model.add(Activation('linear'))

# Define the DeepQTrading class with the following parameters:
# explorations: 0.2 operations are random, and 100 epochs.
# in this case, epochs parameter is used because the Agent acts on a daily basis, 
# so it's better to repeat the experiments several times.
# trainSize: the size of the train data gotten from the dataset, we are setting 5 stock market years, or 1800 days
# validationSize: the size of the validation data gotten from dataset, we are setting 6 stock market months, or 180 days
# testSize: the size of the testing data gotten from dataset, we are setting 6 stock market months, or 180 days
# outputFile: where the results will be written
# begin: where the walks will start from. We are defining January 1st of 2010
# end: where the walks will finish. We are defining February 22nd of 2019
# nOutput: number of walks
dqt = DeepQTrading(
    model=model,
    explorations=[(0.2, 100)],
    trainSize=datetime.timedelta(days=360 * 5),
    validationSize=datetime.timedelta(days=30 * 6),
    testSize=datetime.timedelta(days=30 * 6),
    outputFile="./Output/csv/walks/walks",
    begin=datetime.datetime(2010, 1, 1, 0, 0, 0, 0),
    end=datetime.datetime(2019, 2, 28, 0, 0, 0, 0),
    nbActions=nb_actions,
    isOnlyShort=isOnlyShort,
    ensembleFolderName=sys.argv[3]
)

dqt.run()

dqt.end()
