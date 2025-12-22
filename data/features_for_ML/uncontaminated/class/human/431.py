
class LazyMainAgent:
    def __getattr__(self, name):
        agent = get_main_agent_instance()
        return getattr(agent, name)

    def __call__(self, *args, **kwargs):
        agent = get_main_agent_instance()
        return agent(*args, **kwargs)