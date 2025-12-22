import os
import time
import logging
from typing import Callable, Optional, Dict

class FlowEnvironment:
    '''
    a class to represent the state of the workflow.
    '''

    def __init__(self, name: str, flog=None, fstate=None):
        self.name = name
        self.flog = flog or logging.getLogger(__name__)
        self.fstate = fstate or {}
        self.start_time = time.time()

    def refresh(self, t=None):
        self.fstate['last_refresh'] = t or time.time()

    def kill(self) -> dict:
        self.fstate['killed'] = True
        return self.fstate

    def still_alive(self):
        return not self.fstate.get('killed', False)

    def dump(self):
        return self.fstate

    def run(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    def decorate(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return self.run(func, *args, **kwargs)
        return wrapper

    @staticmethod
    def static_decorate(fstate: Optional[str] = None) -> Callable[..., Callable]:
        def decorator(func):
            def wrapper(*args, **kwargs):
                env = FlowEnvironment('static', fstate=fstate)
                return env.run(func, *args, **kwargs)
            return wrapper
        return decorator

    def __call__(self, func):
        return self.decorate(func)

    def get(self):
        return self.fstate

    def __str__(self):
        return f"FlowEnvironment(name='{self.name}', fstate={self.fstate})"

    def __repr__(self):
        return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.rejuvenate()

    def rejuvenate(self):
        self.fstate = {}
        self.start_time = time.time()