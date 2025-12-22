def find_char_from_name(NAME: str, sim_instance: "Simulator | None" = None):
    if sim_instance is not None:
        for char in sim_instance.characters:
            if char.name == NAME:
                return char
    return None