class _User:
    def __init__(self, data):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'