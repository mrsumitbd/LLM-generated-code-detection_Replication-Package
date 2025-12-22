from typing import Callable, Optional

class FlowEnvironment:
    '''
    a class to represent the state of the workflow.
    '''

    def __init__(self, name: str, flog=None, fstate=None):
        self.name = name
        self.flog = flog
        self.fstate = fstate

    def refresh(self, t=None):
        pass

    def kill(self) -> dict:
        pass

    def still_alive(self):
        pass

    def dump(self):
        pass

    def run(self, func, *args, **kwargs):
        pass

    def decorate(self, func: Callable) -> Callable:
        pass

    @staticmethod
    def static_decorate(fstate: Optional[str] = None) -> Callable[..., Callable]:
        pass

    def __call__(self, func):
        pass

    def get(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def rejuvenate(self):
        pass