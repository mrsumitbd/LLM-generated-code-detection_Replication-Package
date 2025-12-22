class AnimationConfig:
    def __init__(self):
        self.presets = {}

    def get_preset(self, name):
        if name in self.presets:
            return self.presets[name]
        else:
            return None

    def add_preset(self, name, duration, easing):
        self.presets[name] = {
            "duration": duration,
            "easing": easing
        }