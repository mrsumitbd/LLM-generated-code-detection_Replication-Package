import importlib

class LazyMainAgent:
    def __init__(self):
        self._agent = None

    def _load(self):
        if self._agent is None:
            mod = importlib.import_module('main_agent')
            cls = getattr(mod, 'MainAgent')
            self._agent = cls()
        return self._agent

    def __getattr__(self, name):
        agent = self._load()
        return getattr(agent, name)

    def __call__(self, *args, **kwargs):
        agent = self._load()
        return agent(*args, **kwargs)