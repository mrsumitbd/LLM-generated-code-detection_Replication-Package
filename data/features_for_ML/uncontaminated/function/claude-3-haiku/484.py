def print_metrics(metrics, logger, roundto=4):
    for metric, value in metrics.items():
        logger.info(f"{metric.upper()}: {round(value, roundto)}")