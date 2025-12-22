def reset_single_env(env_id, seed):
    import gym
    import numpy as np

    env = gym.make(env_id)
    env.seed(seed)
    np.random.seed(seed)
    
    obs = env.reset()
    
    return env, obs