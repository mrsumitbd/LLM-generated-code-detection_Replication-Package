class ObservationsCfg:
    """Observation specifications for the MDP."""
    
    def __init__(self, observation_space):
        self.observation_space = observation_space
        
    def set_observation_space(self, observation_space):
        self.observation_space = observation_space
        
    def get_observation_space(self):
        return self.observation_space