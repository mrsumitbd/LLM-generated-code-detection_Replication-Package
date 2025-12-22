from __future__ import annotations
from typing import Callable, Iterable, Any, Optional, Dict, Union
import time
import threading


class ComputedBindingConfig:
    """Configuration for computed reactive bindings"""

    def __init__(
        self,
        compute: Callable[..., Any],
        dependencies: Optional[Iterable[str]] = None,
        *,
        lazy: bool = False,
        cache: bool = True,
        debounce: Optional[float] = None,
        throttle: Optional[float] = None,
        immediate: bool = False,
        name: Optional[str] = None,
    ) -> None:
        if not callable(compute):
            raise TypeError("compute must be a callable")
        self.compute: Callable[..., Any] = compute
        self.dependencies: tuple[str, ...] = tuple(dependencies or [])
        self.lazy: bool = lazy
        self.cache: bool = cache
        self.debounce: Optional[float] = debounce
        self.throttle: Optional[float] = throttle
        self.immediate: bool = immediate
        self.name: Optional[str] = name

        # Internal state
        self._cached_value: Any = None
        self._last_run: float = 0.0
        self._debounce_timer: Optional[threading.Timer] = None
        self._lock = threading.RLock()

        if self.immediate:
            self._run_compute()

    def _run_compute(self) -> Any:
        with self._lock:
            self._cached_value = self.compute()
            self._last_run = time.time()
            return self._cached_value

    def get_value(self) -> Any:
        """Return the computed value, respecting cache, debounce, and throttle."""
        with self._lock:
            now = time.time()
            if self.cache and self._cached_value is not None:
                return self._cached_value

            if self.debounce is not None:
                if self._debounce_timer:
                    self._debounce_timer.cancel()
                event = threading.Event()

                def delayed():
                    with self._lock:
                        self._cached_value = self.compute()
                        self._last_run = time.time()
                        event.set()

                self._debounce_timer = threading.Timer(self.debounce, delayed)
                self._debounce_timer.start()
                event.wait()
                return self._cached_value

            if self.throttle is not None and (now - self._last_run) < self.throttle:
                return self._cached_value

            return self._run_compute()

    def invalidate_cache(self) -> None:
        """Clear the cached value."""
        with self._lock:
            self._cached_value = None
            self._last_run = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the config."""
        return {
            "compute": self.compute,
            "dependencies": list(self.dependencies),
            "lazy": self.lazy,
            "cache": self.cache,
            "debounce": self.debounce,
            "throttle": self.throttle,
            "immediate": self.immediate,
            "name": self.name,
        }

    def __repr__(self) -> str:
        parts = [f"{k}={v!r}" for k, v in self.to_dict().items() if k != "compute"]
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComputedBindingConfig):
            return NotImplemented
        return (
            self.compute == other.compute
            and self.dependencies == other.dependencies
            and self.lazy == other.lazy
            and self.cache == other.cache
            and self.debounce == other.debounce
            and self.throttle == other.throttle
            and self.immediate == other.immediate
            and self.name == other.name
        )