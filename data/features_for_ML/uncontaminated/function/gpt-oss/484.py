def print_metrics(metrics, logger, roundto=4):
    """
    Print a collection of metrics using the provided logger.

    Parameters
    ----------
    metrics : dict
        Mapping of metric names to values.
    logger : object
        Logger object that should provide an ``info`` method.
        If the logger does not have an ``info`` method, ``print`` is used.
    roundto : int, optional
        Number of decimal places to round numeric values. Default is 4.
    """
    # Helper to send a message via logger or print
    def _log(msg):
        if hasattr(logger, "info") and callable(logger.info):
            logger.info(msg)
        else:
            print(msg)

    # If metrics is not a dict, just log it directly
    if not isinstance(metrics, dict):
        _log(f"Metrics: {metrics}")
        return

    # Sort keys for deterministic output
    for key in sorted(metrics):
        val = metrics[key]
        # Round numeric values
        if isinstance(val, (int, float)):
            try:
                val_str = f"{round(val, roundto)}"
            except Exception:
                val_str = str(val)
        else:
            val_str = str(val)
        _log(f"{key}: {val_str}")