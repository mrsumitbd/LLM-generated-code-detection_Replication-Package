def get_env_state(self):
    """
    Get the current state of the environment as a dictionary.

    Returns:
        Dict: Contains player position, target position, and hole positions
            as coordinate tuples (row, col)
    """
    # Helper to convert a position to a tuple (row, col)
    def _to_tuple(pos):
        if pos is None:
            return None
        # Accept list, tuple, or any iterable of two numbers
        try:
            return (int(pos[0]), int(pos[1]))
        except Exception:
            return None

    # Retrieve positions from the instance.  The attribute names are
    # chosen to match the most common conventions used in the project.
    # If an attribute is missing, we simply return None for that entry.
    player_pos = getattr(self, "player_pos", None)
    target_pos = getattr(self, "target_pos", None)
    holes = getattr(self, "holes", None)

    # Convert holes to a list of tuples if possible
    hole_positions = []
    if holes is not None:
        try:
            for h in holes:
                hole_positions.append(_to_tuple(h))
        except Exception:
            # If holes is a single position, wrap it
            hole_positions = [_to_tuple(holes)]

    return {
        "player_position": _to_tuple(player_pos),
        "target_position": _to_tuple(target_pos),
        "hole_positions": hole_positions,
    }