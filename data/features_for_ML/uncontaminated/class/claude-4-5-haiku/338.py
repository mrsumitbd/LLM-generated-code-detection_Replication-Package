class ObservationsCfg:
    """Observation specifications for the MDP."""
    
    def __init__(self):
        """Initialize observation configuration."""
        self.observations = {}
    
    def add_observation(self, name: str, spec: dict) -> None:
        """
        Add an observation specification.
        
        Args:
            name: Name of the observation
            spec: Specification dictionary for the observation
        """
        self.observations[name] = spec
    
    def remove_observation(self, name: str) -> None:
        """
        Remove an observation specification.
        
        Args:
            name: Name of the observation to remove
        """
        if name in self.observations:
            del self.observations[name]
    
    def get_observation(self, name: str) -> dict:
        """
        Get an observation specification.
        
        Args:
            name: Name of the observation
            
        Returns:
            Specification dictionary for the observation
        """
        return self.observations.get(name)
    
    def get_all_observations(self) -> dict:
        """
        Get all observation specifications.
        
        Returns:
            Dictionary of all observations
        """
        return self.observations.copy()
    
    def __repr__(self) -> str:
        """Return string representation of the configuration."""
        return f"ObservationsCfg({self.observations})"
    
    def __len__(self) -> int:
        """Return number of observations."""
        return len(self.observations)
    
    def __contains__(self, name: str) -> bool:
        """Check if observation exists."""
        return name in self.observations