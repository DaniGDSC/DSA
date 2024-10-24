import os
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from math import floor

# Deep Q-Learning related imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, LeakyReLU, PReLU
from tensorflow.keras.optimizers import Adam

# RL Agent related imports
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy

# Ensure the directories for output exist
def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Prefix of the name of the market (S&P500) files used to load the data
MK = "dax"

class DeepQTrading:
    def __init__(self, model, explorations, trainSize, validationSize, testSize, outputFile, begin, end, nbActions, isOnlyShort, ensembleFolderName, operationCost=0):
        self.isOnlyShort = isOnlyShort
        self.ensembleFolderName = ensembleFolderName

        # Define the policy, explorations, actions, and model
        self.policy = EpsGreedyQPolicy()
        self.explorations = explorations
        self.nbActions = nbActions
        self.model = model

        # Define memory
        self.memory = SequentialMemory(limit=10000, window_length=1)

        # Instantiate the DQN agent
        self.agent = DQNAgent(model=self.model, policy=self.policy, nb_actions=self.nbActions, memory=self.memory, 
                              nb_steps_warmup=200, target_model_update=1e-1, enable_double_dqn=True, enable_dueling_network=True)

        # Compile the agent
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

        # Save initial weights
        self.agent.save_weights("q.weights", overwrite=True)

        # Set the start and end dates
        self.currentStartingPoint = begin
        self.endingPoint = end

        # Training, validation, and test sizes
        self.trainSize = trainSize
        self.validationSize = validationSize
        self.testSize = testSize
        self.walkSize = trainSize + validationSize + testSize

        # Load the dataset
        self.dates = pd.read_csv('./datasets/' + MK + 'Hour.csv')
        self.sp = pd.read_csv('./datasets/' + MK + 'Hour.csv')
        self.sp['Datetime'] = pd.to_datetime(self.sp['Date'] + ' ' + self.sp['Time'])
        self.sp.set_index('Datetime', inplace=True)
        self.sp.drop(['Time', 'Date'], axis=1, inplace=True)
        self.sp = self.sp.index

        # Operation cost
        self.operationCost = operationCost

        # Initialize callbacks
        self.trainer = ValidationCallback()
        self.validator = ValidationCallback()
        self.tester = ValidationCallback()
        self.outputFileName = outputFile

    def run(self):
        trainEnv = validEnv = testEnv = None
        iteration = -1

        while self.currentStartingPoint + self.walkSize <= self.endingPoint:
            iteration += 1

            # Prepare output file
            self.outputFile = open(self.outputFileName + str(iteration + 1) + ".csv", "w+")
            self.outputFile.write(
                "Iteration,trainAccuracy,trainCoverage,trainReward,trainLong%,trainShort%,trainLongAcc,trainShortAcc,"
                "trainLongPrec,trainShortPrec,validationAccuracy,validationCoverage,validationReward,validationLong%,"
                "validationShort%,validationLongAcc,validationShortAcc,validLongPrec,validShortPrec,testAccuracy,"
                "testCoverage,testReward,testLong%,testShort%,testLongAcc,testShortAcc,testLongPrec,testShortPrec\n")

            # Reset memory and agent
            del self.memory
            del self.agent
            self.memory = SequentialMemory(limit=10000, window_length=1)
            self.agent = DQNAgent(model=self.model, policy=self.policy, nb_actions=self.nbActions, memory=self.memory, 
                                  nb_steps_warmup=200, target_model_update=1e-1, enable_double_dqn=True, enable_dueling_network=True)
            self.agent.compile(Adam(lr=1e-3), metrics=['mae'])
            self.agent.load_weights("q.weights")

            # Perform walk training, validation, and testing
            # Create validation and test files for ensemble
            create_dir_if_not_exists("./Output/ensemble/" + self.ensembleFolderName)
            ensambleValid = pd.DataFrame(index=self.dates.loc[validMinLimit:validMaxLimit, 'Date'].drop_duplicates().tolist())
            ensambleTest = pd.DataFrame(index=self.dates.loc[testMinLimit:testMaxLimit, 'Date'].drop_duplicates().tolist())

            # Train, validate, and test agent as described in the original code
            # ...

            # Close the file
            self.outputFile.close()

            # Update the starting point for the next walk
            self.currentStartingPoint += self.testSize

            # Save validation and test results for ensemble
            ensambleValid.to_csv("./Output/ensemble/" + self.ensembleFolderName + "/walk" + str(iteration) + "ensemble_valid.csv")
            ensambleTest.to_csv("./Output/ensemble/" + self.ensembleFolderName + "/walk" + str(iteration) + "ensemble_test.csv")

    def end(self):
        print("END")
