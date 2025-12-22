import json
import os

class Repo:
    def __init__(self, path, meta=None):
        self.path = os.path.abspath(path)
        if meta is None:
            self.meta = self._load_meta()
        else:
            self.meta = meta

    def _load_meta(self):
        meta_file = os.path.join(self.path, 'meta.json')
        if not os.path.isfile(meta_file):
            raise FileNotFoundError(f"Meta file not found: {meta_file}")
        with open(meta_file, 'r', encoding='utf-8') as f:
            return json.load(f)