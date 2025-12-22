def find_char_from_name(NAME: str, sim_instance: "Simulator | None" = None):
    if sim_instance is None:
        return [char for char in NAME]
    else:
        return [sim_instance.get_character(char) for char in NAME]