class LazyMainAgent:
    def __init__(self):
        self._agent = None

    def _ensure_initialized(self):
        if self._agent is None:
            from anthropic import Anthropic
            self._agent = Anthropic()
        return self._agent

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        agent = self._ensure_initialized()
        return getattr(agent, name)

    def __call__(self, *args, **kwargs):
        agent = self._ensure_initialized()
        return agent(*args, **kwargs)