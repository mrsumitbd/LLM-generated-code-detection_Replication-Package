class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __len__(self):
        return len(self.args)

    def __getitem__(self, index):
        return self.args[index]

    def __iter__(self):
        return iter(self.args)

    def __contains__(self, item):
        return item in self.args

    def __str__(self):
        return f"Args({', '.join(map(str, self.args))})"

    def __repr__(self):
        return f"Args({', '.join(map(repr, self.args))})"

    def get(self, key, default=None):
        return self.kwargs.get(key, default)

    def set(self, key, value):
        self.kwargs[key] = value