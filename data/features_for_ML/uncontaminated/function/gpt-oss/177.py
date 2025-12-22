# Global variable to hold the configuration
_global_config = None

def set_global_config(config: "Config"):
    """
    Set the global configuration object.

    Parameters
    ----------
    config : Config
        The configuration instance to be stored globally.

    Notes
    -----
    This function simply assigns the provided configuration object to a module‑level
    variable.  It does not perform any validation or side effects beyond the
    assignment.  The global variable can be accessed by other parts of the
    application that import this module.
    """
    global _global_config
    _global_config = config