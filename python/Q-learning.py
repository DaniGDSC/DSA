import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
import gym as layers
# Define the environment (simple custom environment or OpenAI Gym environment)
class Environment:
    def __init__(self):
        self.state_space_size = 5  # Example state space size
        self.action_space_size = 3  # Example action space size

    def reset(self):
        return random.randint(0, self.state_space_size - 1)

    def step(self, action):
        next_state = random.randint(0, self.state_space_size - 1)
        reward = random.random()  # Example reward
        done = random.choice([True, False])  # Whether the episode ends
        return next_state, reward, done

# Optimized Deep Q-learning agent using replay memory
class DQNAgent:
    def __init__(self, state_space_size, action_space_size, alpha=0.001, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=2000):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate for epsilon-greedy policy
        self.epsilon_decay = epsilon_decay  # Rate of decay for epsilon
        self.epsilon_min = epsilon_min  # Minimum exploration rate
        self.batch_size = batch_size  # Batch size for experience replay
        self.memory = deque(maxlen=memory_size)  # Replay buffer
        self.model = self.build_model(alpha)  # Neural network model

    def build_model(self, learning_rate):
        # Optimized model with fewer parameters
        model = tf.keras.Sequential([
            layers.Dense(24, input_dim=self.state_space_size, activation='relu'),
            layers.Dense(24, activation='relu'),
            layers.Dense(self.action_space_size, activation='linear')  # Output layer for Q-values of each action
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        # Efficiently add the experience to the memory buffer
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            return random.randint(0, self.action_space_size - 1)  # Explore: random action
        else:
            state = np.reshape(state, [1, self.state_space_size])
            q_values = self.model.predict(state, verbose=0)
            return np.argmax(q_values[0])  # Exploit: select action with max Q-value

    def replay(self):
        # Efficient replay with vectorized operations
        if len(self.memory) < self.batch_size:
            return

        # Randomly sample a batch of experiences
        minibatch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)
        
        # Reshape for efficient matrix operations
        states = np.array(states).reshape(self.batch_size, self.state_space_size)
        next_states = np.array(next_states).reshape(self.batch_size, self.state_space_size)

        # Predict current Q-values and future Q-values for next states
        q_values_current = self.model.predict(states, verbose=0)
        q_values_next = self.model.predict(next_states, verbose=0)

        # Compute the target Q-values
        for i in range(self.batch_size):
            target = rewards[i]
            if not dones[i]:
                target += self.gamma * np.amax(q_values_next[i])
            q_values_current[i][actions[i]] = target

        # Train the model on the updated Q-values
        self.model.fit(states, q_values_current, batch_size=self.batch_size, verbose=0)

    def decay_epsilon(self):
        # Decay epsilon after each episode to reduce exploration
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

# Optimized training function for DQN agent
def train_dqn_agent(episodes=1000):
    env = Environment()
    agent = DQNAgent(state_space_size=env.state_space_size, action_space_size=env.action_space_size)

    for episode in range(episodes):
        state = env.reset()  # Reset environment at the start of each episode
        done = False
        total_reward = 0

        while not done:
            action = agent.choose_action(state)  # Choose an action
            next_state, reward, done = env.step(action)  # Step the environment
            agent.remember(state, action, reward, next_state, done)  # Store experience
            state = next_state  # Move to the next state
            total_reward += reward

            agent.replay()  # Train the model

        agent.decay_epsilon()  # Decay exploration rate

        # Optionally print training progress
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode+1}: Total Reward = {total_reward:.2f}, Epsilon = {agent.epsilon:.4f}")

    return agent

# Train the optimized DQN agent
agent = train_dqn_agent(episodes=1000)

# After training, inspect the model summary
print(agent.model.summary())
