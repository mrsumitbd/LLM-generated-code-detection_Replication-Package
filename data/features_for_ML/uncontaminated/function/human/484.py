def print_metrics(metrics, logger, roundto=4):
    order = sorted(list(metrics.keys()))
    for key in order:
        logger.info(f"{key}: {round(metrics[key], roundto)}")