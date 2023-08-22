import gymnasium as gym
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Multilayer import Multilayer

CHROMSIZE = 24 * 6 + 6 + 6 * 4 + 4
N = 10  # number of episodes to average


env = gym.make("BipedalWalker-v3")  # fitness environment
model = Multilayer(24, 6, 4)  # 8 inputs, 6 hidden neurons, 4 outputs


# phenotype environment
graphical_env = gym.make("BipedalWalker-v3",render_mode="human")
phenotype_model = Multilayer(24, 6, 4)


def step(env, model, observation) -> tuple:
    env.render()
    action = model.inference(observation)
    observation, reward, terminated, truncated, info = env.step(
     action.flatten().tolist())
    return observation, reward, terminated, truncated, info


def phenotype(chromosome):
    observation, info = graphical_env.reset()
    phenotype_model.from_chromosome(chromosome)
    observation, info = graphical_env.reset()
    partial_reward = 0
    while True:
        observation, reward, terminated, truncated, info = step(
            graphical_env, phenotype_model, observation)
        partial_reward += reward
        if terminated or truncated:
            break
    return f'reward: {partial_reward}'


def fitness(chromosome):
    model.from_chromosome(chromosome)
    observation, info = env.reset()
    total_reward = 0
    for _ in range(N):
        partial_reward = 0
        while True:
            observation, reward, terminated, truncated, info = step(
                env, model, observation)
            partial_reward += reward
            if terminated or truncated:
                break
        partial_reward += 400  # add 600 points for each episode
        partial_reward /= 700 # normalize to [0, 1]
        total_reward += partial_reward
    env.close()
    return total_reward / N if total_reward > 0 else 0


parameters = {'alphabet': [-12, 12], 'type': 'floating', 'norm': True, 'chromsize': CHROMSIZE,
              'pmut': 1./(CHROMSIZE), 'popsize': 100, 'trace': 10, 'tournament': 4}
