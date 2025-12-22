import gym
import gymnasium

def reset_single_env(env_id, seed):
    """
    Create a new environment with the given ID, seed it, reset it, and return the environment
    together with the initial observation (and info if available).

    Parameters
    ----------
    env_id : str
        Identifier of the environment to create.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    env : gym.Env or gymnasium.Env
        The created environment instance.
    obs : Any
        The initial observation returned by env.reset().
    info : dict, optional
        Additional info returned by env.reset() (only for gymnasium environments).
    """
    # Try to create the environment using gymnasium first (preferred for newer APIs)
    try:
        env = gymnasium.make(env_id)
        # gymnasium's reset can accept a seed argument
        try:
            obs, info = env.reset(seed=seed)
            return env, obs, info
        except TypeError:
            # Fallback: seed separately
            env.action_space.seed(seed)
            env.observation_space.seed(seed)
            obs = env.reset()
            return env, obs
    except Exception:
        # Fallback to classic gym
        env = gym.make(env_id)
        # Seed the environment
        env.seed(seed)
        env.action_space.seed(seed)
        env.observation_space.seed(seed)
        obs = env.reset()
        return env, obs