import gym

def reset_single_env(env_id, seed):
    env = gym.make(env_id)
    env.seed(seed)
    obs = env.reset()
    return env, obs