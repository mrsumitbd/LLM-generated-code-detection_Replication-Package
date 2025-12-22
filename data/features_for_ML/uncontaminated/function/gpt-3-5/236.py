def get_modal_prefix():
    import os
    import sys
    return os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/'