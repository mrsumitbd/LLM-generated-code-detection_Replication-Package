def _no_need_subversion():
    import sys
    return sys.version_info >= (3, 0)