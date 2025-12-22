def unregister():
    import sys
    import os

    # Get the current module's name
    module_name = sys.modules[__name__].__name__

    # Get the current module's file path
    module_file = sys.modules[__name__].__file__

    # Remove the module from the sys.modules dictionary
    del sys.modules[module_name]

    # Remove the compiled bytecode file (if it exists)
    if os.path.exists(module_file + 'c'):
        os.remove(module_file + 'c')
    if os.path.exists(module_file + 'o'):
        os.remove(module_file + 'o')