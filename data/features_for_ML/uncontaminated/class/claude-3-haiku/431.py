class LazyMainAgent:
    def __init__(self):
        self._agents = {}

    def __getattr__(self, name):
        if name not in self._agents:
            self._agents[name] = Agent(name)
        return self._agents[name]

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    def main(self, *args, **kwargs):
        for agent in self._agents.values():
            agent(*args, **kwargs)


class Agent:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print(f"Executing {self.name} with args={args} and kwargs={kwargs}")