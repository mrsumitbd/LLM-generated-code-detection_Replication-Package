import json
from typing import Any, Dict, Iterable, Iterator, Optional, Tuple


class CurriculumsCfg:
    """Curriculum terms for the MDP."""

    def __init__(self, terms: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the curriculum configuration.

        Parameters
        ----------
        terms : Optional[Dict[str, Any]]
            A mapping from curriculum term names to their configuration.
        """
        self._terms: Dict[str, Any] = dict(terms) if terms else {}

    # ------------------------------------------------------------------
    # Basic container protocol
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._terms)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self._terms.items())

    def __contains__(self, key: str) -> bool:
        return key in self._terms

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._terms!r})"

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def add_term(self, name: str, config: Any) -> None:
        """
        Add or update a curriculum term.

        Parameters
        ----------
        name : str
            The name of the curriculum term.
        config : Any
            The configuration associated with the term.
        """
        if not isinstance(name, str):
            raise TypeError("Curriculum term name must be a string")
        self._terms[name] = config

    def remove_term(self, name: str) -> None:
        """
        Remove a curriculum term.

        Parameters
        ----------
        name : str
            The name of the curriculum term to remove.
        """
        try:
            del self._terms[name]
        except KeyError as exc:
            raise KeyError(f"Curriculum term '{name}' not found") from exc

    def get_term(self, name: str, default: Any = None) -> Any:
        """
        Retrieve a curriculum term configuration.

        Parameters
        ----------
        name : str
            The name of the curriculum term.
        default : Any, optional
            Value to return if the term is not present.

        Returns
        -------
        Any
            The configuration of the requested term or the default.
        """
        return self._terms.get(name, default)

    def list_terms(self) -> Iterable[str]:
        """Return an iterable of all curriculum term names."""
        return self._terms.keys()

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the internal terms dictionary."""
        return dict(self._terms)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurriculumsCfg":
        """Create a new instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
        return cls(terms=data)

    def to_json(self, *, indent: Optional[int] = None) -> str:
        """Serialize the curriculum configuration to a JSON string."""
        return json.dumps(self._terms, indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "CurriculumsCfg":
        """Deserialize a JSON string into a CurriculumsCfg instance."""
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON string") from exc
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def update(self, other: Iterable[Tuple[str, Any]]) -> None:
        """
        Update the curriculum configuration with another iterable of terms.

        Parameters
        ----------
        other : Iterable[Tuple[str, Any]]
            An iterable of (name, config) pairs.
        """
        for name, config in other:
            self.add_term(name, config)

    def clear(self) -> None:
        """Remove all curriculum terms."""
        self._terms.clear()