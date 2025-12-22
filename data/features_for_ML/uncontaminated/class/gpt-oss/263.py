import json
import re
from typing import Any, Dict


class Config:
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    # Optional list of required field names; subclasses may override
    REQUIRED_FIELDS: list[str] = []

    def __init__(self, **kwargs: Any) -> None:
        """Create a Config instance from keyword arguments."""
        self.__dict__.update(kwargs)

    def pretty_print(self, use_color: bool = False) -> str:
        """Return a human‑readable representation of the config.

        Parameters
        ----------
        use_color:
            If True, keys are wrapped in ANSI cyan escape codes.
        """
        data = self.to_dict()
        if use_color:
            # ANSI cyan
            cyan = "\033[96m"
            reset = "\033[0m"

            def colorize(match: re.Match[str]) -> str:
                return f'"{cyan}{match.group(1)}{reset}"'

            # Dump JSON and colorise keys
            raw = json.dumps(data, indent=4)
            return re.sub(r'"(.*?)"(?=\s*:)', colorize, raw)
        else:
            return json.dumps(data, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        """Return the configuration as a plain dictionary."""
        return dict(self.__dict__)

    def validate(self) -> None:
        """Validate the configuration.

        Raises
        ------
        ValueError
            If any required field is missing or any attribute value is None.
        """
        # Ensure no attribute is None
        for name, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"Config attribute '{name}' is None")

        # Ensure all required fields are present
        for field in getattr(self, "REQUIRED_FIELDS", []):
            if not hasattr(self, field):
                raise ValueError(f"Missing required config field: {field}")