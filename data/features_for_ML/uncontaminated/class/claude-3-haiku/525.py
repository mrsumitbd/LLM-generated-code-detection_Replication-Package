import ray
import gym
import numpy as np
from alfworld.agents.utils.env_utils import make_env

class AlfworldWorker:
    """
    Ray remote actor that replaces the worker function.
    Each actor holds one environment instance.
    """

    def __init__(self, config, seed, base_env=None, env_type=None, single_gamefile=None, is_train=True, eval_dataset='eval_in_distribution'):
        self.config = config
        self.seed = seed
        self.base_env = base_env
        self.env_type = env_type
        self.single_gamefile = single_gamefile
        self.is_train = is_train
        self.eval_dataset = eval_dataset

        self.env = make_env(
            config=self.config,
            seed=self.seed,
            base_env=self.base_env,
            env_type=self.env_type,
            single_gamefile=self.single_gamefile,
            is_train=self.is_train,
            eval_dataset=self.eval_dataset
        )

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return obs, reward, done, info

    def reset(self):
        return self.env.reset()

    def getobs(self):
        return self.env.observation_space.sample()