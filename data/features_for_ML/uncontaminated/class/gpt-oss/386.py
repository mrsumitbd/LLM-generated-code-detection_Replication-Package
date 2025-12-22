class RateLimitConfig:
    """
    Configuration for a rate limiter.

    Parameters
    ----------
    max_requests : int, optional
        Maximum number of requests allowed in the period. Default is 100.
    per_seconds : int, optional
        Time window in seconds for the rate limit. Default is 60.
    burst : int, optional
        Maximum burst size. If not provided, defaults to ``max_requests``.
    key : str, optional
        Optional key to identify the rate limit bucket.
    **kwargs
        Any additional configuration options are stored in ``self.extra``.
    """

    def __init__(self, **kwargs):
        # Default values
        defaults = {
            "max_requests": 100,
            "per_seconds": 60,
            "burst": None,
            "key": None,
        }

        # Merge defaults with provided kwargs
        config = {**defaults, **kwargs}

        # Assign attributes
        self.max_requests = int(config["max_requests"])
        self.per_seconds = int(config["per_seconds"])
        self.burst = (
            int(config["burst"])
            if config["burst"] is not None
            else self.max_requests
        )
        self.key = config["key"]

        # Store any extra options
        self.extra = {
            k: v for k, v in config.items() if k not in defaults
        }

        # Basic validation
        if self.max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if self.per_seconds <= 0:
            raise ValueError("per_seconds must be positive")
        if self.burst < self.max_requests:
            raise ValueError("burst must be >= max_requests")

    # ------------------------------------------------------------------
    # Representation & comparison
    # ------------------------------------------------------------------
    def __repr__(self):
        return (
            f"RateLimitConfig(max_requests={self.max_requests}, "
            f"per_seconds={self.per_seconds}, burst={self.burst}, "
            f"key={self.key!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, RateLimitConfig):
            return NotImplemented
        return (
            self.max_requests == other.max_requests
            and self.per_seconds == other.per_seconds
            and self.burst == other.burst
            and self.key == other.key
            and self.extra == other.extra
        )

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self):
        """Return a dictionary representation of the config."""
        data = {
            "max_requests": self.max_requests,
            "per_seconds": self.per_seconds,
            "burst": self.burst,
            "key": self.key,
        }
        data.update(self.extra)
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a RateLimitConfig instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        return cls(**data)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def copy(self):
        """Return a shallow copy of the configuration."""
        return self.__class__(**self.to_dict())