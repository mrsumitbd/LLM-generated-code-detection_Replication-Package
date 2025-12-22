class AnimationConfig:
    def __init__(self):
        self._presets = {}

    def get_preset(self, name):
        return self._presets.get(name)

    def add_preset(self, name, duration, easing):
        self._presets[name] = {"duration": duration, "easing": easing}