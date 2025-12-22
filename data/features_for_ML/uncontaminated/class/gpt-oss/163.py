import time

class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        if hz <= 0:
            raise ValueError("hz must be positive")
        self._period = 1.0 / hz
        # Initialize last_time so that the first call sleeps immediately
        self._last_time = time.perf_counter() - self._period

    def sleep(self, env=None):
        """
        Sleep for the remaining time to maintain the desired rate.

        Parameters
        ----------
        env : optional
            If provided and has a ``timeout`` method (e.g. a SimPy environment),
            the method will return the event created by ``env.timeout``.  If
            ``env`` is None or does not provide ``timeout``, the method will
            block using :func:`time.sleep`.

        Returns
        -------
        event or None
            The event returned by ``env.timeout`` if an environment is
            supplied and supports it; otherwise ``None``.
        """
        now = time.perf_counter()
        elapsed = now - self._last_time
        sleep_time = self._period - elapsed

        if sleep_time > 0:
            if env is not None and hasattr(env, "timeout"):
                # Return the event so the caller can yield it
                return env.timeout(sleep_time)
            else:
                time.sleep(sleep_time)

        # Update the timestamp for the next cycle
        self._last_time = time.perf_counter()
        return None