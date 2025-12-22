from typing import List

def initialize_app(param: ApplicationConfig, args: List[str] = None):
    """Initialize app
    If you use gunicorn as a process manager, initialize_app can be invoke in
    `on_starting` hook.
    Args:
        param:WebWerverParameters
        args:List[str]
    """
    # Your implementation goes here
    pass