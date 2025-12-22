def get_env_state(self):
    """
    Get the current state of the environment as a dictionary.
    
    Returns:
        Dict: Contains player position, target position, and hole positions
            as coordinate tuples (row, col)
    """
    return {
        'player_pos': self.player_pos,
        'target_pos': self.target_pos,
        'hole_positions': self.hole_positions
    }