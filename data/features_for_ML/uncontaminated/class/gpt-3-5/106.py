import json

class Repo:

    def __init__(self, path, meta=None):
        self.path = path
        self.meta = meta
        if self.meta is None:
            self._load_meta()

    def _load_meta(self):
        with open(self.path, 'r') as file:
            self.meta = json.load(file)