class Repo:

    def __init__(self, path, meta=None):
        self.path = path
        self.meta = meta if meta is not None else self._load_meta()

    def _load_meta(self):
        import json
        import os
        
        meta_path = os.path.join(self.path, '.meta')
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}