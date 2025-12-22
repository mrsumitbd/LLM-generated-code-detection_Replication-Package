class LazyMainAgent:
    
    def __init__(self):
        self.attributes = {}

    def __getattr__(self, name):
        if name not in self.attributes:
            self.attributes[name] = None
        return self.attributes[name]

    def __call__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.attributes[key] = value