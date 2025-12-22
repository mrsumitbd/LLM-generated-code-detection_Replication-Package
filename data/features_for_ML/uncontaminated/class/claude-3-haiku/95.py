import numpy as np
from gym.spaces import Box

class VectorizedGemEnv:
    def __init__(self, num_envs=8, seed=None):
        self.num_envs = num_envs
        self.seed = seed
        self.action_space = Box(low=-1, high=1, shape=(num_envs, 2), dtype=np.float32)
        self.observation_space = Box(low=-1, high=1, shape=(num_envs, 4), dtype=np.float32)
        self.reset()

    def reset(self):
        self.states = np.random.uniform(-1, 1, size=(self.num_envs, 4))
        return self.states

    def step(self, actions):
        assert actions.shape == (self.num_envs, 2)
        next_states = self.states + actions
        rewards = np.sum(np.square(next_states), axis=1)
        dones = np.zeros(self.num_envs, dtype=bool)
        self.states = next_states
        return self.states, rewards, dones, {}

    def render(self, mode='human'):
        pass

    def close(self):
        pass