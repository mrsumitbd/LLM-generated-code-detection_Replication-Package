from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, Qt, pyqtProperty, QPoint, QRect

class AnimationConfig:
    def __init__(self):
        self.presets = {
            "fast": {"duration": 200, "easing": QEasingCurve.OutCubic},
            "normal": {"duration": 500, "easing": QEasingCurve.InOutCubic},
            "slow": {"duration": 800, "easing": QEasingCurve.InOutQuad},
            "bounce": {"duration": 600, "easing": QEasingCurve.OutBounce},
            "elastic": {"duration": 800, "easing": QEasingCurve.OutElastic},
            "smooth": {"duration": 400, "easing": QEasingCurve.InOutQuad},
        }
    def get_preset(self, name):
        return self.presets.get(name, self.presets["normal"])
    def add_preset(self, name, duration, easing):
        self.presets[name] = {"duration": duration, "easing": easing}