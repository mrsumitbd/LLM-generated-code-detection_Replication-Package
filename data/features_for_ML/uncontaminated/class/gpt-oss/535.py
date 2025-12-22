from __future__ import annotations
from typing import Any, Dict, Mapping, MutableMapping


class SummaryResults:
    """
    A lightweight container for summary data that can be serialised to JSON.
    """

    def __init__(self, data: Mapping[str, Any] | None = None, **kwargs: Any) -> None:
        """
        Initialise the container with optional mapping or keyword arguments.

        Parameters
        ----------
        data : Mapping[str, Any] | None
            Optional initial data mapping.
        **kwargs : Any
            Optional keyword arguments to initialise the container.
        """
        self._data: MutableMapping[str, Any] = {}
        if data is not None:
            self._data.update(data)
        if kwargs:
            self._data.update(kwargs)

    def to_json_dict(self) -> Dict[str, Any]:
        """
        Return a plain dictionary representation suitable for JSON serialisation.

        Returns
        -------
        Dict[str, Any]
            A shallow copy of the internal data dictionary.
        """
        return dict(self._data)

    # Optional convenience methods
    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"