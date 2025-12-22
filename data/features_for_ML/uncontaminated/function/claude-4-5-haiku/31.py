def unregister():
    import atexit
    import sys
    
    # Get the current frame to find the calling module
    frame = sys._getframe(1)
    module_name = frame.f_globals.get('__name__')
    
    # Unregister the module from sys.modules if it exists
    if module_name and module_name in sys.modules:
        del sys.modules[module_name]
    
    # Remove any atexit handlers registered by the module
    if hasattr(atexit, '_registry'):
        atexit._registry[:] = [
            handler for handler in atexit._registry
            if handler[0].__module__ != module_name
        ]