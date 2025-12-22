class CurriculumsCfg:
    """Curriculum terms for the MDP."""
    
    def __init__(self):
        """Initialize curriculum configuration."""
        self.curricula = {}
    
    def add_curriculum(self, name: str, curriculum: dict) -> None:
        """Add a curriculum to the configuration.
        
        Args:
            name: Name of the curriculum
            curriculum: Dictionary containing curriculum configuration
        """
        self.curricula[name] = curriculum
    
    def get_curriculum(self, name: str) -> dict:
        """Get a curriculum by name.
        
        Args:
            name: Name of the curriculum
            
        Returns:
            Dictionary containing curriculum configuration
        """
        return self.curricula.get(name)
    
    def remove_curriculum(self, name: str) -> bool:
        """Remove a curriculum by name.
        
        Args:
            name: Name of the curriculum
            
        Returns:
            True if curriculum was removed, False otherwise
        """
        if name in self.curricula:
            del self.curricula[name]
            return True
        return False
    
    def list_curricula(self) -> list:
        """List all curriculum names.
        
        Returns:
            List of curriculum names
        """
        return list(self.curricula.keys())
    
    def update_curriculum(self, name: str, updates: dict) -> bool:
        """Update an existing curriculum.
        
        Args:
            name: Name of the curriculum
            updates: Dictionary of updates to apply
            
        Returns:
            True if curriculum was updated, False otherwise
        """
        if name in self.curricula:
            self.curricula[name].update(updates)
            return True
        return False
    
    def clear_curricula(self) -> None:
        """Clear all curricula."""
        self.curricula.clear()
    
    def __repr__(self) -> str:
        """Return string representation of the configuration."""
        return f"CurriculumsCfg(curricula={self.curricula})"
    
    def __len__(self) -> int:
        """Return number of curricula."""
        return len(self.curricula)