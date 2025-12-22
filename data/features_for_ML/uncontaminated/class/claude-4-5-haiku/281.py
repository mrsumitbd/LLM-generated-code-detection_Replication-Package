class CommandsCfg:
    """Command terms for the MDP."""
    
    def __init__(self):
        """Initialize the CommandsCfg with default command terms."""
        self.commands = {}
    
    def add_command(self, name: str, value: any) -> None:
        """Add a command term to the configuration.
        
        Args:
            name: The name of the command.
            value: The value associated with the command.
        """
        self.commands[name] = value
    
    def get_command(self, name: str) -> any:
        """Retrieve a command term from the configuration.
        
        Args:
            name: The name of the command to retrieve.
            
        Returns:
            The value associated with the command, or None if not found.
        """
        return self.commands.get(name)
    
    def remove_command(self, name: str) -> bool:
        """Remove a command term from the configuration.
        
        Args:
            name: The name of the command to remove.
            
        Returns:
            True if the command was removed, False if it didn't exist.
        """
        if name in self.commands:
            del self.commands[name]
            return True
        return False
    
    def list_commands(self) -> list:
        """List all available commands.
        
        Returns:
            A list of all command names.
        """
        return list(self.commands.keys())
    
    def clear_commands(self) -> None:
        """Clear all commands from the configuration."""
        self.commands.clear()
    
    def __repr__(self) -> str:
        """Return a string representation of the CommandsCfg."""
        return f"CommandsCfg({self.commands})"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        if not self.commands:
            return "CommandsCfg: No commands configured"
        commands_str = ", ".join(f"{k}: {v}" for k, v in self.commands.items())
        return f"CommandsCfg: {commands_str}"