def print_metrics(metrics, logger, roundto=4):
    for key, value in metrics.items():
        logger.info(f"{key}: {round(value, roundto)}")