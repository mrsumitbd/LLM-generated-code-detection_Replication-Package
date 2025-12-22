class Select:
    def __init__(self, *args):
        self.columns = args

    def __call__(self, data):
        return [{key: row[key] for key in self.columns} for row in data]