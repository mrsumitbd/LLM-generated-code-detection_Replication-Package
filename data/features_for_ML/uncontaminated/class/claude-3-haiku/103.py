class _LogConfig:
    """Parsed configuration from PYTHON_LOG: default level and per-pattern rules."""

    def __init__(self):
        self.default_level = None
        self.rules = []

    def add_rule(self, pattern, level):
        self.rules.append((pattern, level))

    def get_level(self, name):
        for pattern, level in self.rules:
            if name.startswith(pattern):
                return level
        return self.default_level