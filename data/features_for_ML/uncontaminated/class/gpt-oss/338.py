import json
from collections.abc import Mapping, Iterable
from copy import deepcopy
from typing import Any, Dict, Iterable, Tuple, Union


class ObservationsCfg:
    """Observation specifications for the MDP."""

    def __init__(self, specs: Mapping[str, Any] | None = None):
        """
        Parameters
        ----------
        specs : Mapping[str, Any] | None
            Optional initial mapping of observation names to their specifications.
            Each specification should be a mapping containing at least the keys
            ``shape`` and ``dtype``.  Additional keys such as ``bounds`` are
            allowed.
        """
        self._specs: Dict[str, Dict[str, Any]] = {}
        if specs:
            for name, spec in specs.items():
                self.add_spec(name, **spec)

    # ------------------------------------------------------------------
    # Basic container protocol
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._specs)

    def __iter__(self) -> Iterable[str]:
        return iter(self._specs)

    def __contains__(self, name: str) -> bool:
        return name in self._specs

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._specs!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ObservationsCfg) and self._specs == other._specs

    # ------------------------------------------------------------------
    # Specification manipulation
    # ------------------------------------------------------------------
    def add_spec(
        self,
        name: str,
        shape: Union[Tuple[int, ...], Iterable[int]],
        dtype: str = "float32",
        bounds: Tuple[Union[float, int], Union[float, int]] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Add or replace an observation specification.

        Parameters
        ----------
        name : str
            Name of the observation.
        shape : tuple[int, ...] | Iterable[int]
            Shape of the observation array.
        dtype : str, optional
            Data type of the observation.  Defaults to ``"float32"``.
        bounds : tuple[float, float] | None, optional
            Optional lower and upper bounds for the observation values.
        **kwargs : Any
            Additional keyword arguments are stored verbatim in the spec.
        """
        spec: Dict[str, Any] = {
            "shape": tuple(shape),
            "dtype": dtype,
        }
        if bounds is not None:
            if not (isinstance(bounds, tuple) and len(bounds) == 2):
                raise ValueError("bounds must be a tuple of length 2")
            spec["bounds"] = tuple(bounds)
        spec.update(kwargs)
        self._specs[name] = spec

    def get_spec(self, name: str) -> Dict[str, Any] | None:
        """
        Retrieve the specification for a given observation name.

        Parameters
        ----------
        name : str
            Observation name.

        Returns
        -------
        dict | None
            The specification dictionary or ``None`` if the name is not present.
        """
        return deepcopy(self._specs.get(name))

    def remove_spec(self, name: str) -> None:
        """
        Remove an observation specification.

        Parameters
        ----------
        name : str
            Observation name to remove.
        """
        self._specs.pop(name, None)

    def clear(self) -> None:
        """Remove all observation specifications."""
        self._specs.clear()

    def update(self, other: Mapping[str, Any]) -> None:
        """
        Update the configuration with another mapping of specifications.

        Parameters
        ----------
        other : Mapping[str, Any]
            Mapping of observation names to specifications.
        """
        for name, spec in other.items():
            self.add_spec(name, **spec)

    # ------------------------------------------------------------------
    # Validation utilities
    # ------------------------------------------------------------------
    def validate(self, name: str, data: Any) -> bool:
        """
        Validate a data sample against the stored specification.

        Parameters
        ----------
        name : str
            Observation name.
        data : Any
            Data sample to validate.

        Returns
        -------
        bool
            ``True`` if the data matches the specification, otherwise ``False``.
        """
        spec = self._specs.get(name)
        if spec is None:
            raise KeyError(f"Specification for observation '{name}' not found")

        # Shape check
        try:
            shape = tuple(data.shape)
        except AttributeError:
            # Not array-like
            return False
        if shape != spec["shape"]:
            return False

        # Dtype check
        dtype = getattr(data, "dtype", None)
        if dtype is None:
            return False
        if str(dtype) != spec["dtype"]:
            return False

        # Bounds check
        bounds = spec.get("bounds")
        if bounds is not None:
            low, high = bounds
            if data.min() < low or data.max() > high:
                return False

        return True

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Return a deep copy of the internal specification dictionary."""
        return deepcopy(self._specs)

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "ObservationsCfg":
        """Create a new instance from a dictionary of specifications."""
        return cls(deepcopy(d))

    def to_json(self) -> str:
        """Serialize the configuration to a JSON string."""
        return json.dumps(self._specs)

    @classmethod
    def from_json(cls, s: str) -> "ObservationsCfg":
        """Deserialize a JSON string into a new configuration instance."""
        return cls(json.loads(s))

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------
    @property
    def names(self) -> Tuple[str, ...]:
        """Return a tuple of all observation names."""
        return tuple(self._specs.keys())

    def shape(self, name: str) -> Tuple[int, ...]:
        """Return the shape of the specified observation."""
        spec = self._specs.get(name)
        if spec is None:
            raise KeyError(f"Specification for observation '{name}' not found")
        return spec["shape"]

    def dtype(self, name: str) -> str:
        """Return the dtype of the specified observation."""
        spec = self._specs.get(name)
        if spec is None:
            raise KeyError(f"Specification for observation '{name}' not found")
        return spec["dtype"]

    def bounds(self, name: str) -> Tuple[Union[float, int], Union[float, int]] | None:
        """Return the bounds of the specified observation, if any."""
        spec = self._specs.get(name)
        if spec is None:
            raise KeyError(f"Specification for observation '{name}' not found")
        return spec.get("bounds")