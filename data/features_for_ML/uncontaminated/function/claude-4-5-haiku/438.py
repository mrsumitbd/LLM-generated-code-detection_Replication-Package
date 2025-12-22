def reset_single_env(env_id, seed):
    import gymnasium as gym
    
    env = gym.make(env_id)
    env.reset(seed=seed)
    return env