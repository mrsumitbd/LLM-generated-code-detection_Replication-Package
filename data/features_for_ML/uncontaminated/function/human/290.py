import logging

def setup_logging(verbose=False):
	logger.handlers.clear()

	handler = logging.StreamHandler()
	formatter = logging.Formatter("%(levelname)s: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	if verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	# Prevent propagation to root logger (no third-party logs)
	logger.propagate = False

	# Globally disable all third-party logging
	logging.getLogger().handlers.clear()
	logging.getLogger().setLevel(logging.CRITICAL + 1)