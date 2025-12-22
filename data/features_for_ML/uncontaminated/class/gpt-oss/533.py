class RolloutEnvState:
    """Per-environment variables for the rollout loop."""

    def __init__(self, observation=None, reward=0.0, done=False, info=None, step=0, action=None):
        """
        Initialize the state for a single environment.

        Parameters
        ----------
        observation : Any, optional
            The initial observation returned by the environment.
        reward : float, optional
            The initial reward (default 0.0).
        done : bool, optional
            Whether the episode is finished (default False).
        info : dict, optional
            Additional info dictionary (default empty dict).
        step : int, optional
            The current step count (default 0).
        action : Any, optional
            The last action taken (default None).
        """
        self.observation = observation
        self.reward = reward
        self.done = done
        self.info = info if info is not None else {}
        self.step = step
        self.action = action

    # ------------------------------------------------------------------
    # State manipulation helpers
    # ------------------------------------------------------------------
    def reset(self, observation):
        """
        Reset the state to the beginning of a new episode.

        Parameters
        ----------
        observation : Any
            The observation returned by the environment after reset.
        """
        self.observation = observation
        self.reward = 0.0
        self.done = False
        self.info = {}
        self.step = 0
        self.action = None

    def step_update(self, observation, reward, done, info, action):
        """
        Update the state after taking a step in the environment.

        Parameters
        ----------
        observation : Any
            The new observation returned by the environment.
        reward : float
            The reward received from the environment.
        done : bool
            Whether the episode has terminated.
        info : dict
            Additional info dictionary returned by the environment.
        action : Any
            The action that was taken.
        """
        self.observation = observation
        self.reward = reward
        self.done = done
        self.info = info
        self.step += 1
        self.action = action

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def to_dict(self):
        """Return a dictionary representation of the state."""
        return {
            "observation": self.observation,
            "reward": self.reward,
            "done": self.done,
            "info": self.info,
            "step": self.step,
            "action": self.action,
        }

    def __repr__(self):
        return (
            f"RolloutEnvState(step={self.step}, done={self.done}, "
            f"reward={self.reward}, action={self.action})"
        )