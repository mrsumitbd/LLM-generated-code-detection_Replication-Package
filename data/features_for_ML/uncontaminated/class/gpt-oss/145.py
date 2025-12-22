class NumberFormatConfig:
    """Configuration for Count Bits dataset generation"""

    def __init__(
        self,
        bit_width: int = 8,
        min_value: int = 0,
        max_value: int | None = None,
        seed: int | None = None,
        fmt: str = "binary",
    ):
        self.bit_width = bit_width
        self.min_value = min_value
        self.max_value = max_value
        self.seed = seed
        self.format = fmt

    def validate(self) -> bool:
        """Validate the configuration values.

        Raises:
            ValueError: If any configuration value is invalid.
        Returns:
            bool: True if validation passes.
        """
        # Validate bit_width
        if not isinstance(self.bit_width, int) or self.bit_width <= 0:
            raise ValueError("bit_width must be a positive integer")

        # Determine maximum possible value for the given bit width
        max_possible = (1 << self.bit_width) - 1

        # Validate max_value
        if self.max_value is None:
            self.max_value = max_possible
        if not isinstance(self.max_value, int):
            raise ValueError("max_value must be an integer")
        if not (0 <= self.max_value <= max_possible):
            raise ValueError(
                f"max_value must be between 0 and {max_possible} for bit_width {self.bit_width}"
            )

        # Validate min_value
        if not isinstance(self.min_value, int):
            raise ValueError("min_value must be an integer")
        if not (0 <= self.min_value <= self.max_value):
            raise ValueError(
                f"min_value must be between 0 and max_value ({self.max_value})"
            )

        # Validate seed
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")

        # Validate format
        allowed_formats = {"binary", "decimal", "hex"}
        if self.format not in allowed_formats:
            raise ValueError(
                f"format must be one of {sorted(allowed_formats)}; got {self.format!r}"
            )

        return True