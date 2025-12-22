from typing import Callable, Optional
import time
import threading
from datetime import datetime


class FlowEnvironment:
    '''
    a class to represent the state of the workflow.
    '''

    def __init__(self, name: str, flog=None, fstate=None):
        self.name = name
        self.flog = flog if flog is not None else []
        self.fstate = fstate if fstate is not None else {}
        self.start_time = datetime.now()
        self.end_time = None
        self.is_alive = True
        self._lock = threading.Lock()

    def refresh(self, t=None):
        with self._lock:
            if t is not None:
                self.fstate['last_refresh'] = t
            else:
                self.fstate['last_refresh'] = datetime.now()

    def kill(self) -> dict:
        with self._lock:
            self.is_alive = False
            self.end_time = datetime.now()
            return {
                'name': self.name,
                'status': 'killed',
                'start_time': self.start_time,
                'end_time': self.end_time
            }

    def still_alive(self):
        with self._lock:
            return self.is_alive

    def dump(self):
        with self._lock:
            return {
                'name': self.name,
                'flog': self.flog.copy() if isinstance(self.flog, list) else self.flog,
                'fstate': self.fstate.copy() if isinstance(self.fstate, dict) else self.fstate,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'is_alive': self.is_alive
            }

    def run(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            self.flog.append({
                'function': func.__name__,
                'status': 'success',
                'timestamp': datetime.now(),
                'result': result
            })
            return result
        except Exception as e:
            self.flog.append({
                'function': func.__name__,
                'status': 'error',
                'timestamp': datetime.now(),
                'error': str(e)
            })
            raise

    def decorate(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return self.run(func, *args, **kwargs)
        return wrapper

    @staticmethod
    def static_decorate(fstate: Optional[str] = None) -> Callable[..., Callable]:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def __call__(self, func):
        return self.decorate(func)

    def get(self):
        with self._lock:
            return self.fstate

    def __str__(self):
        return f"FlowEnvironment(name='{self.name}', alive={self.is_alive}, logs={len(self.flog)})"

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        self.refresh()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.flog.append({
                'status': 'exception',
                'timestamp': datetime.now(),
                'exception_type': exc_type.__name__,
                'exception_value': str(exc_value)
            })
        return False

    def rejuvenate(self):
        with self._lock:
            self.is_alive = True
            self.start_time = datetime.now()
            self.end_time = None
            self.flog = []
            self.fstate = {}