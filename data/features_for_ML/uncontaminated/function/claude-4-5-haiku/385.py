def find_char_from_name(NAME: str, sim_instance: "Simulator | None" = None):
    """
    Find a character object from a name string.
    
    Args:
        NAME: The name of the character to find
        sim_instance: Optional simulator instance to search within
        
    Returns:
        The character object if found, None otherwise
    """
    if sim_instance is None:
        return None
    
    # Search through characters in the simulator instance
    if hasattr(sim_instance, 'characters'):
        for char in sim_instance.characters:
            if hasattr(char, 'name') and char.name == NAME:
                return char
    
    # Alternative: search through a characters dictionary if it exists
    if hasattr(sim_instance, 'character_dict'):
        return sim_instance.character_dict.get(NAME)
    
    # Alternative: search through active characters
    if hasattr(sim_instance, 'active_characters'):
        for char in sim_instance.active_characters:
            if hasattr(char, 'name') and char.name == NAME:
                return char
    
    return None