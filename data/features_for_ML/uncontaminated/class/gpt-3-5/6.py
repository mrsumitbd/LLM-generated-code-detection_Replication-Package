class ComputedBindingConfig:
    def __init__(self, update_on_change=False, debounce_time=None):
        self.update_on_change = update_on_change
        self.debounce_time = debounce_time

    def __str__(self):
        return f"ComputedBindingConfig(update_on_change={self.update_on_change}, debounce_time={self.debounce_time})"