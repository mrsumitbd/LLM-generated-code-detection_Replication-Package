class _User:
    def __init__(self, data):
        self.data = data
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"_User({self.data})"