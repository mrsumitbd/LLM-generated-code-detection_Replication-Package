def find_char_from_name(NAME: str, sim_instance: "Simulator | None" = None):
    """
    Find and return a character object from the simulator instance by its name.

    Parameters
    ----------
    NAME : str
        The name (or a substring of the name) of the character to find.
    sim_instance : Simulator | None, optional
        The simulator instance that contains the characters. If None, a
        ValueError is raised.

    Returns
    -------
    character | None
        The character object that matches the given name, or None if no match
        is found.
    """
    if sim_instance is None:
        raise ValueError("sim_instance must be provided")

    # Try to obtain the list of characters from the simulator.
    # Different simulators may expose the characters in different ways.
    chars = None
    if hasattr(sim_instance, "characters"):
        chars = sim_instance.characters
    elif hasattr(sim_instance, "get_characters"):
        chars = sim_instance.get_characters()
    elif hasattr(sim_instance, "get_all_characters"):
        chars = sim_instance.get_all_characters()
    else:
        # If we cannot find a character list, raise an informative error.
        raise AttributeError(
            "The simulator instance does not expose a character list "
            "via 'characters', 'get_characters', or 'get_all_characters'."
        )

    # Ensure we have an iterable of characters.
    if chars is None:
        return None

    # Normalize the search string for case‑insensitive comparison.
    target = NAME.strip().lower()

    # First pass: look for an exact match (case‑insensitive).
    for char in chars:
        # Assume each character has a 'name' attribute.
        if hasattr(char, "name"):
            if getattr(char, "name", "").strip().lower() == target:
                return char

    # Second pass: look for a partial match (substring).
    for char in chars:
        if hasattr(char, "name"):
            if target in getattr(char, "name", "").strip().lower():
                return char

    # No match found.
    return None