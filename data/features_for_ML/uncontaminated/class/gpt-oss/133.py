from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union


@dataclass
class OnnxExportArguments:
    """
    Arguments to decide how the ModelProto will be saved.

    The class is intentionally lightweight and serialisable.  All fields are
    optional and have sensible defaults that match the behaviour of
    :func:`torch.onnx.export` and :func:`onnx.save`.

    Attributes
    ----------
    opset_version : int
        The ONNX opset version to target.  Must be a positive integer.
    export_params : bool
        If ``True`` the model's parameters are exported as initializers.
    keep_initializers_as_inputs : bool
        If ``True`` initializers are also added to the graph inputs.
    input_names : Optional[List[str]]
        Names of the model inputs.  If ``None`` the names are inferred from
        the model.
    output_names : Optional[List[str]]
        Names of the model outputs.  If ``None`` the names are inferred from
        the model.
    dynamic_axes : Optional[Dict[str, Dict[int, str]]]
        Mapping from input/output names to a mapping of dimension indices to
        names.  Used to declare dynamic shapes.
    custom_opsets : Optional[Dict[str, int]]
        Mapping from domain names to opset versions for custom ops.
    verbose : bool
        If ``True`` prints progress information during export.
    training : str
        One of ``"none"``, ``"training"``, or ``"inference"`` to indicate the
        training mode of the exported graph.
    """

    opset_version: int = 13
    export_params: bool = True
    keep_initializers_as_inputs: bool = False
    input_names: Optional[List[str]] = None
    output_names: Optional[List[str]] = None
    dynamic_axes: Optional[Dict[str, Dict[int, str]]] = None
    custom_opsets: Optional[Dict[str, int]] = None
    verbose: bool = False
    training: str = "none"

    def __post_init__(self) -> None:
        # Validate opset_version
        if not isinstance(self.opset_version, int) or self.opset_version <= 0:
            raise ValueError(
                f"opset_version must be a positive integer, got {self.opset_version!r}"
            )

        # Validate booleans
        for name in ("export_params", "keep_initializers_as_inputs", "verbose"):
            value = getattr(self, name)
            if not isinstance(value, bool):
                raise TypeError(f"{name} must be a bool, got {value!r}")

        # Validate input_names / output_names
        for name in ("input_names", "output_names"):
            value = getattr(self, name)
            if value is not None:
                if not isinstance(value, (list, tuple)):
                    raise TypeError(f"{name} must be a list or tuple of strings")
                for idx, item in enumerate(value):
                    if not isinstance(item, str):
                        raise TypeError(
                            f"{name}[{idx}] must be a string, got {item!r}"
                        )

        # Validate dynamic_axes
        if self.dynamic_axes is not None:
            if not isinstance(self.dynamic_axes, dict):
                raise TypeError("dynamic_axes must be a dict")
            for key, val in self.dynamic_axes.items():
                if not isinstance(key, str):
                    raise TypeError(f"dynamic_axes key must be a string, got {key!r}")
                if not isinstance(val, dict):
                    raise TypeError(
                        f"dynamic_axes[{key!r}] must be a dict, got {val!r}"
                    )
                for dim_idx, dim_name in val.items():
                    if not isinstance(dim_idx, int):
                        raise TypeError(
                            f"dynamic_axes[{key!r}][{dim_idx!r}] must be an int"
                        )
                    if not isinstance(dim_name, str):
                        raise TypeError(
                            f"dynamic_axes[{key!r}][{dim_idx!r}] must be a string"
                        )

        # Validate custom_opsets
        if self.custom_opsets is not None:
            if not isinstance(self.custom_opsets, dict):
                raise TypeError("custom_opsets must be a dict")
            for domain, version in self.custom_opsets.items():
                if not isinstance(domain, str):
                    raise TypeError(f"custom_opsets key must be a string, got {domain!r}")
                if not isinstance(version, int) or version <= 0:
                    raise ValueError(
                        f"custom_opsets[{domain!r}] must be a positive integer, got {version!r}"
                    )

        # Validate training
        if self.training not in {"none", "training", "inference"}:
            raise ValueError(
                f"training must be one of 'none', 'training', or 'inference', got {self.training!r}"
            )

    # --------------------------------------------------------------------- #
    # Convenience helpers
    # --------------------------------------------------------------------- #

    def to_dict(self) -> Dict[str, Union[int, bool, List[str], Dict, str]]:
        """
        Return a dictionary representation of the arguments, omitting
        ``None`` values.
        """
        result: Dict[str, Union[int, bool, List[str], Dict, str]] = {
            "opset_version": self.opset_version,
            "export_params": self.export_params,
            "keep_initializers_as_inputs": self.keep_initializers_as_inputs,
            "verbose": self.verbose,
            "training": self.training,
        }
        if self.input_names is not None:
            result["input_names"] = list(self.input_names)
        if self.output_names is not None:
            result["output_names"] = list(self.output_names)
        if self.dynamic_axes is not None:
            result["dynamic_axes"] = {
                k: dict(v) for k, v in self.dynamic_axes.items()
            }
        if self.custom_opsets is not None:
            result["custom_opsets"] = dict(self.custom_opsets)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "OnnxExportArguments":
        """
        Construct an :class:`OnnxExportArguments` instance from a dictionary.
        """
        return cls(
            opset_version=data.get("opset_version", 13),
            export_params=data.get("export_params", True),
            keep_initializers_as_inputs=data.get("keep_initializers_as_inputs", False),
            input_names=data.get("input_names"),
            output_names=data.get("output_names"),
            dynamic_axes=data.get("dynamic_axes"),
            custom_opsets=data.get("custom_opsets"),
            verbose=data.get("verbose", False),
            training=data.get("training", "none"),
        )

    def __repr__(self) -> str:
        args = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({args})"