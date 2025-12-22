import logging
import signal

# Configure a logger for this module.  The caller can adjust the level
# or handler as needed.
_logger = logging.getLogger(__name__)


def graceful_signal_handler(signum, frame):
    """
    Custom signal handler to gracefully handle SIGTERM when Locust is already shutting down.
    This prevents the "stopping state" exception from being raised.

    The handler simply logs the receipt of the signal and ignores it.  If the
    signal arrives while Locust is in the process of shutting down, the
    default behaviour would raise a ``LocustStoppingException``.  By
    intercepting the signal here we avoid that exception and allow the
    shutdown to complete cleanly.

    Parameters
    ----------
    signum : int
        The signal number (e.g., ``signal.SIGTERM``).
    frame : types.FrameType
        The current stack frame (unused).
    """
    # Log the signal for debugging purposes.
    _logger.debug(
        "Received SIGTERM (signal %s) during shutdown; ignoring to avoid "
        "LocustStoppingException.", signum
    )

    # Reset the handler for SIGTERM to the default or ignore it for any
    # subsequent signals.  This is defensive: if another SIGTERM arrives
    # while we are still shutting down, we simply ignore it.
    try:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    except Exception:
        # In some environments (e.g., Windows) signal handling may be
        # limited; ignore any errors.
        pass

    # No further action is required – simply return to allow the
    # shutdown process to continue.
    return