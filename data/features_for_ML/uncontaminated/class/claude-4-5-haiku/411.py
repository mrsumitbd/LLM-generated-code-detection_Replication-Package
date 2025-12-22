class PoseObservationsCfg:
    """Observation specifications for the environment."""
    
    def __init__(self):
        """Initialize pose observations configuration."""
        self.observations = {}
    
    def add_observation(self, name: str, spec: dict) -> None:
        """Add an observation specification.
        
        Args:
            name: Name of the observation
            spec: Specification dictionary for the observation
        """
        self.observations[name] = spec
    
    def get_observation(self, name: str) -> dict:
        """Get an observation specification by name.
        
        Args:
            name: Name of the observation
            
        Returns:
            Specification dictionary for the observation
        """
        return self.observations.get(name)
    
    def remove_observation(self, name: str) -> None:
        """Remove an observation specification.
        
        Args:
            name: Name of the observation to remove
        """
        if name in self.observations:
            del self.observations[name]
    
    def list_observations(self) -> list:
        """List all observation names.
        
        Returns:
            List of observation names
        """
        return list(self.observations.keys())
    
    def __repr__(self) -> str:
        """Return string representation of the configuration."""
        return f"PoseObservationsCfg(observations={self.observations})"
    
    def __len__(self) -> int:
        """Return number of observations."""
        return len(self.observations)