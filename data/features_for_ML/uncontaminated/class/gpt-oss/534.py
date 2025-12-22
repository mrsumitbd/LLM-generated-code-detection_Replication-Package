import torch
from pathlib import Path
from typing import Any, Dict


class T3Cond:
    """
    Dataclass container for most / all conditioning info.
    TODO: serialization methods aren't used, keeping them around for convenience
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Create a container with arbitrary attributes.

        Parameters
        ----------
        **kwargs
            Any conditioning information to store as attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def _move_obj(self, obj: Any, device: Any = None, dtype: Any = None) -> Any:
        """
        Recursively move tensors to the specified device/dtype.
        """
        if isinstance(obj, torch.Tensor):
            return obj.to(device=device, dtype=dtype)
        if isinstance(obj, dict):
            return {k: self._move_obj(v, device, dtype) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set)):
            return type(obj)(self._move_obj(v, device, dtype) for v in obj)
        return obj

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def to(self, *, device: Any = None, dtype: Any = None) -> "T3Cond":
        """
        Move all tensor attributes to the given device and/or dtype.

        Parameters
        ----------
        device
            Target device (e.g., 'cpu', 'cuda:0').
        dtype
            Target dtype (e.g., torch.float32).

        Returns
        -------
        T3Cond
            The instance itself (modified in place).
        """
        for attr in list(self.__dict__.keys()):
            setattr(self, attr, self._move_obj(getattr(self, attr), device, dtype))
        return self

    def save(self, fpath: str | Path) -> None:
        """
        Serialize the conditioning information to a file.

        Parameters
        ----------
        fpath
            Path to the file where the data will be stored.
        """
        torch.save(self.__dict__, Path(fpath))

    @staticmethod
    def load(fpath: str | Path, map_location: Any = "cpu") -> "T3Cond":
        """
        Load conditioning information from a file.

        Parameters
        ----------
        fpath
            Path to the file containing the serialized data.
        map_location
            Device mapping for loaded tensors.

        Returns
        -------
        T3Cond
            A new instance populated with the loaded data.
        """
        data: Dict[str, Any] = torch.load(Path(fpath), map_location=map_location)
        return T3Cond(**data)