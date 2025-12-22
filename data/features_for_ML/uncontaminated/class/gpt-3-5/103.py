class _LogConfig:
    def __init__(self, default_level, per_pattern_rules):
        self.default_level = default_level
        self.per_pattern_rules = per_pattern_rules

    def get_default_level(self):
        return self.default_level

    def get_per_pattern_rules(self):
        return self.per_pattern_rules