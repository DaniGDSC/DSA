# Copyright (C) 2020 Salvatore Carta, Anselmo Ferreira, Alessandro Sebastian Podda,
# Diego Reforgiato Recupero, Antonio Sanna. All rights reserved.

# Imports the SPEnv library, which will perform the Agent actions themselves
from spEnv import SpEnv

# Callback used to print the results at each episode
from callback import ValidationCallback

# TensorFlow Keras for the NN considered
import tensorflow as tf
from tensorflow.keras.models import Sequential
# TensorFlow Keras libraries for layers, activations, and optimizers
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import LeakyReLU, PReLU
from tensorflow.keras.optimizers import Adam

# RL Agent
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy

# Mathematical operations used later
from math import floor

# Library to manipulate the dataset in a CSV file
import pandas as pd

# Library used to manipulate time
import datetime


# Prefix of the name of the market (S&P500) files used to load the data
MK = "dax"

class DeepQTrading:
    
    # Class constructor
    def __init__(self, model, explorations, trainSize, validationSize, testSize, outputFile, begin, end, nbActions, isOnlyShort, ensembleFolderName, operationCost=0):
        
        self.isOnlyShort = isOnlyShort
        self.ensembleFolderName = ensembleFolderName

        # Define the policy, explorations, actions, and model as received by parameters
        self.policy = EpsGreedyQPolicy()
        self.explorations = explorations
        self.nbActions = nbActions
        self.model = model

        # Define the memory
        self.memory = SequentialMemory(limit=10000, window_length=1)

        # Instantiate the agent with parameters received
        self.agent = DQNAgent(model=self.model, policy=self.policy, nb_actions=self.nbActions, memory=self.memory, nb_steps_warmup=200, target_model_update=1e-1,
                              enable_double_dqn=True, enable_dueling_network=True)
        
        # Compile the agent with the Adam optimizer and mean absolute error metric
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

        # Save the weights of the agents in the q.weights file
        self.agent.save_weights("q.weights", overwrite=True)

        # Define the current starting point as the initial date
        self.currentStartingPoint = begin

        # Define the training, validation, and testing sizes
        self.trainSize = trainSize
        self.validationSize = validationSize
        self.testSize = testSize
        
        # The walk size is train + validation + test sizes
        self.walkSize = trainSize + validationSize + testSize
        
        # Define the ending point as the final date
        self.endingPoint = end

        # Read the hourly dataset
        self.dates = pd.read_csv('./datasets/' + MK + 'Hour.csv')
        self.sp = pd.read_csv('./datasets/' + MK + 'Hour.csv')

        # Convert the pandas format to date and time format
        self.sp['Datetime'] = pd.to_datetime(self.sp['Date'] + ' ' + self.sp['Time'])
        
        # Set an index to Datetime on the pandas-loaded dataset
        self.sp = self.sp.set_index('Datetime')
        
        # Drop Time and Date from the Dataset
        self.sp = self.sp.drop(['Time', 'Date'], axis=1)

        # Receive the operation cost (transaction fees), set to 0
        self.operationCost = operationCost
        
        # Call the callback for training, validation, and testing to show results for each episode
        self.trainer = ValidationCallback()
        self.validator = ValidationCallback()
        self.tester = ValidationCallback()
        self.outputFileName = outputFile

    def run(self):
        # Initialize environments
        trainEnv = validEnv = testEnv = " "
        iteration = -1

        # While all the walks are not finished
        while(self.currentStartingPoint + self.walkSize <= self.endingPoint):
            iteration += 1
            self.outputFile = open(self.outputFileName + str(iteration + 1) + ".csv", "w+")
            self.outputFile.write("Iteration,trainAccuracy,trainCoverage,trainReward,trainLong%,trainShort%,trainLongAcc,trainShortAcc,trainLongPrec,trainShortPrec,validationAccuracy,"
                                  "validationCoverage,validationReward,validationLong%,validationShort%,validationLongAcc,validationShortAcc,validLongPrec,validShortPrec,"
                                  "testAccuracy,testCoverage,testReward,testLong%,testShort%,testLongAcc,testShortAcc,testLongPrec,testShortPrec\n")

            # Reset memory and agent for each iteration
            del(self.memory)
            del(self.agent)

            self.memory = SequentialMemory(limit=10000, window_length=1)
            self.agent = DQNAgent(model=self.model, policy=self.policy, nb_actions=self.nbActions, memory=self.memory, nb_steps_warmup=200, target_model_update=1e-1,
                                  enable_double_dqn=True, enable_dueling_network=True)
            self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

            # Load the saved weights
            self.agent.load_weights("q.weights")

            # Determine the training, validation, and test limits
            trainMinLimit = self._get_limit(self.currentStartingPoint)
            trainMaxLimit = self._get_limit(self.currentStartingPoint + self.trainSize)
            validMinLimit = trainMaxLimit + 1
            validMaxLimit = self._get_limit(self.currentStartingPoint + self.trainSize + self.validationSize)
            testMinLimit = validMaxLimit + 1
            testMaxLimit = self._get_limit(self.currentStartingPoint + self.trainSize + self.validationSize + self.testSize)

            ensambleValid = pd.DataFrame(index=self.dates[validMinLimit:validMaxLimit].ix[:, 'Date'].drop_duplicates().tolist())
            ensambleTest = pd.DataFrame(index=self.dates[testMinLimit:testMaxLimit].ix[:, 'Date'].drop_duplicates().tolist())
            ensambleValid.index.name = 'Date'
            ensambleTest.index.name = 'Date'

            for eps in self.explorations:
                self.policy.eps = eps[0]

                for i in range(0, eps[1]):
                    trainEnv = SpEnv(operationCost=self.operationCost, minLimit=trainMinLimit, maxLimit=trainMaxLimit, callback=self.trainer, isOnlyShort=self.isOnlyShort)
                    validEnv = SpEnv(operationCost=self.operationCost, minLimit=validMinLimit, maxLimit=validMaxLimit, callback=self.validator, isOnlyShort=self.isOnlyShort, ensamble=ensambleValid, columnName="iteration"+str(i))
                    testEnv = SpEnv(operationCost=self.operationCost, minLimit=testMinLimit, maxLimit=testMaxLimit, callback=self.tester, isOnlyShort=self.isOnlyShort, ensamble=ensambleTest, columnName="iteration"+str(i))

                    self._train_and_evaluate(i, trainEnv, validEnv, testEnv)

            self.outputFile.close()
            self.currentStartingPoint += self.testSize

            ensambleValid.to_csv("./Output/ensemble/" + self.ensembleFolderName + "/walk" + str(iteration) + "ensemble_valid.csv")
            ensambleTest.to_csv("./Output/ensemble/" + self.ensembleFolderName + "/walk" + str(iteration) + "ensemble_test.csv")

    def _get_limit(self, date):
        # Safely retrieves the limit for the dataset index based on the date
        limit = None
        while limit is None:
            try:
                limit = self.sp.get_loc(date)
            except:
                date += datetime.timedelta(0, 0, 0, 0, 0, 1, 0)
        return limit

    def _train_and_evaluate(self, iteration, trainEnv, validEnv, testEnv):
        # Train and evaluate the model
        self.trainer.reset()
        self.agent.fit(trainEnv, nb_steps=floor(self.trainSize.days - self.trainSize.days * 0.2), visualize=False, verbose=0)
        train_metrics = self.trainer.getInfo()

        self.validator.reset()
        self.agent.test(validEnv, nb_episodes=floor(self.validationSize.days - self.validationSize.days * 0.2), visualize=False, verbose=0)
        valid_metrics = self.validator.getInfo()

        self.tester.reset()
        self.agent.test(testEnv, nb_episodes=floor(self.validationSize.days - self.validationSize.days * 0.2), visualize=False, verbose=0)
        test_metrics = self.tester.getInfo()

        # Save results
        self._log_results(iteration, train_metrics, valid_metrics, test_metrics)

    def _log_results(self, iteration, train_metrics, valid_metrics, test_metrics):
        # Write the results to a CSV file
        self.outputFile.write(
            str(iteration) + "," +
            ",".join(map(str, train_metrics)) + "," +
            ",".join(map(str, valid_metrics)) + "," +
            ",".join(map(str, test_metrics)) + "\n")

    def end(self):
        print("END")
