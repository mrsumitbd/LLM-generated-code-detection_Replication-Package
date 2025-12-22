def get_options(options_or_path):
    if isinstance(options_or_path, dict):
        return options_or_path
    elif isinstance(options_or_path, str):
        with open(options_or_path, 'r') as file:
            options = json.load(file)
        return options