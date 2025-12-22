class ObservationsCfg:
    """Observation specifications for the MDP."""

    def __init__(self, observation_dim, observation_low, observation_high):
        self.observation_dim = observation_dim
        self.observation_low = observation_low
        self.observation_high = observation_high

    def get_observation_space(self):
        """Returns the observation space as a gym.spaces.Box."""
        return gym.spaces.Box(low=self.observation_low, high=self.observation_high, shape=(self.observation_dim,))

    def sample_observation(self):
        """Samples a random observation from the observation space."""
        return np.random.uniform(low=self.observation_low, high=self.observation_high, size=(self.observation_dim,))