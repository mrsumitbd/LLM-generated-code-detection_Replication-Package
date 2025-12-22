import os
import toml

class ConfigManager:
    """Handles loading, accessing, and updating the Pylings configuration from `pylings.toml`."""

    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'pylings.toml')
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            return toml.load(f)

    def check_first_time(self):
        return self.config.get('first_time', True)

    def get_lasttime_exercise(self):
        return self.config.get('last_exercise', None)

    def set_lasttime_exercise(self, current_exercise):
        self.config['last_exercise'] = current_exercise
        self.save_config()

    def get_local_solution_path(self, solution_path):
        return os.path.join(os.path.dirname(__file__), self.config['solution_path'], solution_path)

    def get_hint(self, current_exercise):
        return self.config['exercises'][current_exercise]['hint']

    def save_config(self):
        with open(self.config_file, 'w') as f:
            toml.dump(self.config, f)