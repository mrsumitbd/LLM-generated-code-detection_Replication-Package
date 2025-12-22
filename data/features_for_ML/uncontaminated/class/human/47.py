import json
from functools import wraps
import logging
import time
from typing import Callable, Dict, Optional

class FlowEnvironment:
    '''
    a class to represent the state of the workflow.
    '''
    def __init__(self, name: str, flog=None, fstate=None):
        '''
        instantiate the FlowEnvironment with a name and an optional log file.
        
        Parameters
        ----------
        name : str
            The name of the workflow.
        flog : str, optional
            The log file to record the workflow state. If None, no logging is performed.
        '''
        self.name = name
        self.state = {
            'workflow': self.name,
            'start_time': time.strftime("%Y.%m.%d %H:%M:%S"),
            'end_time': None,
            'results': [],
            'flog': flog
        }
        self.fstate = fstate
        self.avail = True
        # initialize the logging if flog is provided
        if flog is not None:
            logging.basicConfig(
                filename=flog, 
                level=logging.ERROR,
                format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info(f"Workflow {self.name} initialized at "
                         f"{self.state['start_time']}")
    
    def refresh(self, t=None):
        '''
        refresh the time
        '''
        if self.still_alive():
            self.state['end_time'] = t \
                if t is not None else time.strftime("%Y.%m.%d %H:%M:%S")
            logging.info(f"Workflow {self.name} refreshed at "
                         f"{self.state['end_time']}")
        else:
            logging.warning(f"Workflow {self.name} is not available, "
                            f"cannot refresh the state.")
    
    def kill(self) -> dict:
        '''
        end the workflow and return the state.
        '''
        self.refresh()
        self.avail = False
        logging.info(f"Workflow {self.name} killed at "
                     f"{self.state['end_time']}")
        logging.shutdown()
        return self.state
    
    def still_alive(self):
        '''
        check the status of the workflow.
        Returns True if the workflow is available, False otherwise.
        '''
        logging.info(f"Checking if workflow {self.name} is still alive."
            f": {self.avail}")
        return self.avail
    
    def dump(self):
        '''
        dump the state to a json file.
        if fn is None, dump to a file named by the workflow name.
        '''
        if self.fstate is not None:
            # fn = f'{self.name}-{time.strftime("%Y%m%d-%H%M%S")}.json'
        
            with open(self.fstate, 'w') as f:
                json.dump(self.state, f, indent=4)
        
        return self.state
    
    def run(self, func, *args, **kwargs):
        '''
        run a function and record the state.
        '''
        if not self.still_alive():
            logging.error(f"Workflow {self.name} is not available, "
                          f"cannot run the function.")
            return self.state
        
        # if the environment is still alive
        task_name = func.__name__ if hasattr(func, '__name__') \
            else str(func)
        _t = time.time()
        
        # there are cases that user call this function like
        # env.run(func(1, 2)), what is really passed is the
        # result of the function, not the function itself.
        if not callable(func):
            self.state['results'].append(
                {
                    'task': task_name,
                    'return': func,
                    'args': args,
                    'kwargs': kwargs,
                    'duration': time.time() - _t,
                    'exception': []
                }
            )
            logging.warning(f"Function {task_name} is not callable, "
                           f"returning the result directly.")
            self.refresh()
            return func
        
        # callable case, error catching is needed
        base = {
            'task': task_name,
            'args': args,
            'kwargs': kwargs,
            'duration': None,
            'exception': []
        }
        try:
            result = func(*args, **kwargs)
            self.state['results'].append(
                {
                    **base,
                    'return': result,
                    'duration': time.time() - _t,
                    'exception': []
                }
            )
            logging.info(f"Function {task_name} executed successfully, "
                         f"returning the result.")
            return result
        except Exception as e:
            self.state['results'].append(
                {
                    **base,
                    'return': None,
                    'duration': time.time() - _t,
                    'exception': str(e)
                }
            )
            logging.error(f"Function {task_name} raised an exception: {e}")
            # if an exception occurs, kill the environment
            self.kill()
            return self.state
        finally:
            self.refresh()
            # refresh the end time after the function is executed
        
    # support the decorator protocol
    def decorate(self, func: Callable) -> Callable:
        '''
        a decorator to run a function within the environment. All
        functions will be recorded in the environment state. A 
        manually dump is needed to save the state to a file.
        
        Parameters
        ----------
        func : Callable
            The function to be decorated.

        Returns
        -------
        Callable
            A wrapper function that runs the original function within
            a FlowEnvironment instance. The wrapped function will 
            return the state dict if the function is not callable,
            or any exception occurs during the execution. If there
            is no exception, the wrapped function will return the
            return value of the original function.
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.run(func, *args, **kwargs)
        return wrapper
    
    @staticmethod
    def static_decorate(fstate: Optional[str] = None) -> Callable[..., Callable]:
        '''
        a static implementation of the decorator to run a function.
        The function will be recorded in its own environment state.
        Once the function is returned, the state dict will be dumped
        to a file named by the function name.
        
        Parameters
        ----------
        fstate : Optional[str], optional
            The file name to dump the state. If None, a default name
            will be generated based on the function name and current
            timestamp. Default is None.
        
        Returns
        -------
        Callable
            A wrapper function that runs the original function within
            a FlowEnvironment instance and dumps the state to a file.
            If any exception occurs during the execution, the state
            dict will be returned instead of the function's return value.
        '''
        def decorator(func: Callable) -> Callable:
            myname = func.__name__
            myfstate = fstate or \
                f'pyfunc-{myname}-{time.strftime("%Y%m%d%H%M%S")}.json'
            @wraps(func)
            def wrapper(*args, **kwargs):
                # create a FlowEnvironment instance with the function name
                env = FlowEnvironment(name=myname, fstate=myfstate)
                result = env.run(func, *args, **kwargs)
                # dump the state to a file named by the function name and
                # close the environment
                env.dump()
                return result.copy() if isinstance(result, dict) else result
            return wrapper
        return decorator
    
    def __call__(self, func):
        '''
        make the FlowEnvironment callable, so that it can be used as a decorator.
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.run(func, *args, **kwargs)
        return wrapper
    
    def get(self):
        '''
        get the `return` value of the last run function.
        '''
        if not self.state['results']:
            return None
        return self.state['results'][-1].get('return', None)

    def __str__(self):
        myself = '\nABACUS Agent Flow Environment\n'
        myself +=  '-----------------------------\n'
        myself += f'Workflow Name: {self.name}\n'
        myself += f'Start Time: {self.state["start_time"]}\n'
        myself += f'End Time: {self.state["end_time"]}\n'
        myself += f'Still Alive: {self.still_alive()}\n'
        myself += f'Results:\n'
        for res in self.state['results']:
            myself += f'  - Task: {res["task"]}\n'
            myself += f'    Return: {res.get("return", None)}\n'
            myself += f'    Duration: {res["duration"]}\n'
            myself += f'    Exception: {res["exception"]}\n'
            myself += f'    Args: {res["args"]}\n'
            myself += f'    Kwargs: {res["kwargs"]}\n'
        return myself

    def __repr__(self):
        return self.__str__()
    
    # support the context manager protocol
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''
        exit of the context manager.
        If an exception occurs, kill the environment.
        If no exception occurs, just refresh the environment.
        '''
        if exc_type is not None:
            self.kill()
        else:
            self.refresh()

    def rejuvenate(self):
        '''
        rejuvinate the environment, i.e., reset the state.
        
        Returns
        -------
        dict
            The previous state of the environment before rejuvenation.
        '''
        mymemory = self.dump().copy()
        
        # reset the state
        self.state = {
            'workflow': self.name,
            'start_time': time.strftime("%Y.%m.%d %H:%M:%S"),
            'end_time': None,
            'results': [],
            'flog': self.state.get('flog', None)
        }
        self.avail = True
        logging.info(f"Workflow {self.name} rejuvenated at "
                     f"{self.state['start_time']}")
        return mymemory