import gym
import numpy as np

class VectorizedGemEnv:

    def __init__(self, env_name, num_envs):
        self.envs = [gym.make(env_name) for _ in range(num_envs)]
        self.num_envs = num_envs

    def reset(self):
        return np.array([env.reset() for env in self.envs])

    def step(self, actions):
        next_states, rewards, dones, infos = [], [], [], []
        for env, action in zip(self.envs, actions):
            next_state, reward, done, info = env.step(action)
            next_states.append(next_state)
            rewards.append(reward)
            dones.append(done)
            infos.append(info)
        return np.array(next_states), np.array(rewards), np.array(dones), infos

    def close(self):
        for env in self.envs:
            env.close()