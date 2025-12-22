def initialize_app(param: ApplicationConfig, args: List[str] = None):
    """Initialize app
    If you use gunicorn as a process manager, initialize_app can be invoke in
    `on_starting` hook.
    Args:
        param:WebWerverParameters
        args:List[str]
    """
    if args is None:
        args = []
    
    # Initialize configuration
    if hasattr(param, 'config'):
        for key, value in param.config.items():
            if value is not None:
                setattr(param, key, value)
    
    # Initialize logging if available
    if hasattr(param, 'setup_logging'):
        param.setup_logging()
    
    # Initialize database connections if available
    if hasattr(param, 'init_db'):
        param.init_db()
    
    # Initialize cache if available
    if hasattr(param, 'init_cache'):
        param.init_cache()
    
    # Process command line arguments
    if args:
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                if hasattr(param, key):
                    setattr(param, key, value)
    
    # Call any custom initialization hooks
    if hasattr(param, 'on_init'):
        param.on_init()