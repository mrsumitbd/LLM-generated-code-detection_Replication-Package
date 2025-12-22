import toml

class ConfigManager:
    """Handles loading, accessing, and updating the Pylings configuration from `pylings.toml`."""

    def __init__(self):
        self.config = None

    def load_config(self):
        with open('pylings.toml', 'r') as file:
            self.config = toml.load(file)

    def check_first_time(self):
        return self.config.get('first_time', True)

    def get_lasttime_exercise(self):
        return self.config.get('lasttime_exercise', None)

    def set_lasttime_exercise(self, current_exercise):
        self.config['lasttime_exercise'] = current_exercise

    def get_local_solution_path(self, solution_path):
        return self.config.get('local_solution_path', {}).get(solution_path, None)

    def get_hint(self, current_exercise):
        return self.config.get('hints', {}).get(current_exercise, None)