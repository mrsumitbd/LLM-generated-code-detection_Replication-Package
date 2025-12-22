import threading
import time
import logging

class WatchDog:
    """
    A simple watchdog that runs a target callable in a separate thread and
    automatically restarts it if it terminates. The watchdog itself runs in
    its own thread and checks the target thread at a configurable interval.
    """

    def __init__(self, target, interval=5, name=None, **kwargs):
        """
        Parameters
        ----------
        target : callable
            The function or callable object to run under watchdog supervision.
        interval : float, optional
            Seconds between checks of the target thread. Default is 5.
        name : str, optional
            Optional name for the watchdog thread.
        **kwargs
            Keyword arguments passed to the target callable.
        """
        if not callable(target):
            raise TypeError("target must be callable")

        self._target = target
        self._interval = float(interval)
        self._target_kwargs = kwargs
        self._name = name or f"WatchDog-{id(self)}"

        self._target_thread = None
        self._watch_thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._running = False

        self._logger = logging.getLogger(self._name)

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _run_target(self):
        """Execute the target callable."""
        try:
            self._logger.debug("Target thread starting.")
            self._target(**self._target_kwargs)
            self._logger.debug("Target thread finished normally.")
        except Exception as exc:
            self._logger.exception("Target thread raised an exception: %s", exc)

    def _watch(self):
        """Watchdog loop that restarts the target thread if needed."""
        self._logger.debug("Watchdog thread started.")
        while not self._stop_event.is_set():
            with self._lock:
                if self._target_thread is None or not self._target_thread.is_alive():
                    self._logger.info("Restarting target thread.")
                    self._target_thread = threading.Thread(
                        target=self._run_target,
                        name=f"{self._name}-Target",
                        daemon=True,
                    )
                    self._target_thread.start()
            time.sleep(self._interval)
        self._logger.debug("Watchdog thread exiting.")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def start(self):
        """Start the watchdog and the target thread."""
        with self._lock:
            if self._running:
                self._logger.warning("Watchdog already running.")
                return
            self._stop_event.clear()
            self._watch_thread = threading.Thread(
                target=self._watch,
                name=self._name,
                daemon=True,
            )
            self._watch_thread.start()
            self._running = True
            self._logger.info("Watchdog started.")

    def stop(self):
        """Stop the watchdog and wait for threads to finish."""
        with self._lock:
            if not self._running:
                self._logger.warning("Watchdog not running.")
                return
            self._stop_event.set()
            self._running = False

        if self._watch_thread:
            self._watch_thread.join()
            self._watch_thread = None

        if self._target_thread:
            # We cannot forcibly kill a thread in Python; we simply wait for it.
            self._target_thread.join()
            self._target_thread = None

        self._logger.info("Watchdog stopped.")

    def restart(self):
        """
        Force a restart of the target thread on the next watchdog cycle.
        The current target thread will be allowed to finish naturally.
        """
        with self._lock:
            self._target_thread = None
            self._logger.info("Target thread will be restarted on next cycle.")

    @property
    def running(self):
        """Return True if the watchdog is currently running."""
        return self._running

    @property
    def target_thread(self):
        """Return the current target thread (or None)."""
        return self._target_thread

    @property
    def watch_thread(self):
        """Return the watchdog thread (or None)."""
        return self._watch_thread