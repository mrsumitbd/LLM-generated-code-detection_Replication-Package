from typing import Any, Dict, List, Union


class ActionInfo:
    """Complete action information with binding support"""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize an ActionInfo instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments that become attributes of the instance.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def bind(self, **bindings: Any) -> None:
        """
        Bind or update attributes of the instance.

        Parameters
        ----------
        **bindings
            Keyword arguments to bind or update on the instance.
        """
        for key, value in bindings.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ActionInfo instance into a plain dictionary.

        Nested ActionInfo objects are recursively converted to dictionaries.
        Lists containing ActionInfo objects are also converted element‑wise.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        def _convert(value: Any) -> Any:
            if isinstance(value, ActionInfo):
                return value.to_dict()
            if isinstance(value, list):
                return [_convert(v) for v in value]
            if isinstance(value, dict):
                return {k: _convert(v) for k, v in value.items()}
            return value

        # Exclude private attributes (starting with an underscore)
        return {
            key: _convert(value)
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }