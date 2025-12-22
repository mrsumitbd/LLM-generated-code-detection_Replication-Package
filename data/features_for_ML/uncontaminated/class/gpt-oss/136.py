from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ClientCapability:
    """Represents client capabilities.

    Capabilities are stored as key/value pairs.  The class is intentionally
    lightweight and flexible – it can be used to hold any number of
    capabilities that a client might expose.
    """

    _capabilities: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __init__(self, **kwargs: Any) -> None:
        """Create a new :class:`ClientCapability` instance.

        Parameters
        ----------
        **kwargs
            Arbitrary capability name/value pairs.
        """
        for key, value in kwargs.items():
            self._capabilities[key] = value

    def add(self, name: str, value: Any) -> None:
        """Add or update a capability.

        Parameters
        ----------
        name
            The capability name.
        value
            The capability value.
        """
        self._capabilities[name] = value

    def remove(self, name: str) -> None:
        """Remove a capability if it exists.

        Parameters
        ----------
        name
            The capability name to remove.
        """
        self._capabilities.pop(name, None)

    def get(self, name: str, default: Any | None = None) -> Any | None:
        """Retrieve a capability value.

        Parameters
        ----------
        name
            The capability name.
        default
            Value to return if the capability is not present.

        Returns
        -------
        Any
            The capability value or ``default``.
        """
        return self._capabilities.get(name, default)

    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the capabilities dictionary."""
        return dict(self._capabilities)