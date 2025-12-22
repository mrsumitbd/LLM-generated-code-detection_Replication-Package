class JsonHParams:

    def __init__(self, **kwargs):
        self.params = kwargs

    def keys(self):
        return self.params.keys()

    def items(self):
        return self.params.items()

    def values(self):
        return self.params.values()

    def __len__(self):
        return len(self.params)

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __contains__(self, key):
        return key in self.params

    def __repr__(self):
        return f'JsonHParams({self.params})'