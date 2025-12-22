class ChromeConfig:
    """Configuration for Chrome driver."""

    def __init__(self, executable_path, options=None):
        self.executable_path = executable_path
        self.options = options or []

    def add_option(self, option):
        self.options.append(option)

    def remove_option(self, option):
        self.options.remove(option)

    def get_options(self):
        return self.options

    def get_executable_path(self):
        return self.executable_path