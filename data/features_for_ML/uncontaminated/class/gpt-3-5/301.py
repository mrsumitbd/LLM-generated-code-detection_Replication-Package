class AnimationConfig:
    
    def __init__(self):
        self.presets = {}

    def get_preset(self, name):
        return self.presets.get(name)

    def add_preset(self, name, duration, easing):
        self.presets[name] = {'duration': duration, 'easing': easing}