import logging
import contextvars

# A thread‑local (context‑local) storage for log context data
_log_context = contextvars.ContextVar("log_context", default={})


class LogContext:
    """
    A context manager that temporarily injects key/value pairs into the
    logging context.  The values are available to any logging filter that
    inspects the current context.
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._token = None

    def __enter__(self):
        # Merge the new context with the current one
        current = _log_context.get()
        new_context = current.copy()
        new_context.update(self._kwargs)
        # Store the token so we can restore the previous context later
        self._token = _log_context.set(new_context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the previous context
        if self._token is not None:
            _log_context.reset(self._token)

    @staticmethod
    def get_context():
        """Return the current logging context dictionary."""
        return _log_context.get()


class ContextFilter(logging.Filter):
    """
    A logging filter that injects the current context into each LogRecord.
    """
    def filter(self, record):
        ctx = LogContext.get_context()
        for key, value in ctx.items():
            setattr(record, key, value)
        return True