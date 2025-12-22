import random
import numpy as np

class AlfworldWorker:
    """
    Ray remote actor that replaces the worker function.
    Each actor holds one environment instance.
    """

    def __init__(self, config, seed, base_env=None, env_type=None,
                 single_gamefile=None, is_train=True, eval_dataset='eval_in_distribution'):
        """
        Initialize the worker with a single environment instance.

        Parameters
        ----------
        config : dict
            Configuration dictionary for the environment.
        seed : int
            Random seed for reproducibility.
        base_env : gym.Env, optional
            Pre‑created environment instance. If provided, it will be used directly.
        env_type : str, optional
            Name of the environment type to create if `base_env` is None.
        single_gamefile : str, optional
            Path to a single game file for the environment.
        is_train : bool, optional
            Flag indicating whether the worker is used for training.
        eval_dataset : str, optional
            Identifier for the evaluation dataset.
        """
        self.config = config
        self.seed = seed
        self.is_train = is_train
        self.eval_dataset = eval_dataset

        # If a base environment is provided, use it; otherwise create a new one.
        if base_env is not None:
            self.env = base_env
        else:
            # Attempt to create an environment based on env_type or single_gamefile.
            # This is a placeholder; replace with actual environment creation logic.
            try:
                import gym
                if env_type is not None:
                    self.env = gym.make(env_type, **config)
                elif single_gamefile is not None:
                    # Assume the environment can be created from a game file.
                    self.env = gym.make("AlfworldEnv-v0", game_file=single_gamefile, **config)
                else:
                    # Default environment
                    self.env = gym.make("AlfworldEnv-v0", **config)
            except Exception:
                # Fallback: create a dummy environment that mimics gym.Env
                class DummyEnv:
                    def reset(self):
                        return np.zeros((10,))

                    def step(self, action):
                        return np.zeros((10,)), 0.0, False, {}

                    def seed(self, seed):
                        random.seed(seed)
                        np.random.seed(seed)

                self.env = DummyEnv()

        # Seed the environment for reproducibility
        try:
            self.env.seed(self.seed)
        except Exception:
            pass

        # Store the current observation
        self.obs = None

    def step(self, action):
        """
        Take a step in the environment using the provided action.

        Parameters
        ----------
        action : any
            Action to apply in the environment.

        Returns
        -------
        obs : any
            Observation after the action.
        reward : float
            Reward received.
        done : bool
            Whether the episode has terminated.
        info : dict
            Additional information.
        """
        obs, reward, done, info = self.env.step(action)
        self.obs = obs
        return obs, reward, done, info

    def reset(self):
        """
        Reset the environment to an initial state.

        Returns
        -------
        obs : any
            Initial observation after reset.
        """
        self.obs = self.env.reset()
        return self.obs

    def getobs(self):
        """
        Retrieve the most recent observation.

        Returns
        -------
        obs : any
            Current observation.
        """
        return self.obs