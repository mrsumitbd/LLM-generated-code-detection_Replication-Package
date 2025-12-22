import os
import json

class Repo:
    def __init__(self, path, meta=None):
        self.path = path
        self.meta = meta or self._load_meta()

    def _load_meta(self):
        meta_file = os.path.join(self.path, '.repo_meta.json')
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                return json.load(f)
        else:
            return {}