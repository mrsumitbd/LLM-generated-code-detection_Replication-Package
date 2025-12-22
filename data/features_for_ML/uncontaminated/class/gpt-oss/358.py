from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# The following enums are assumed to be defined elsewhere in the project.
# They are imported here for type checking purposes only.
try:
    from .quantization import QuantFormat, QuantizationMode, QuantType
except Exception:  # pragma: no cover
    # Minimal stubs for type checking / documentation purposes
    from enum import Enum

    class QuantFormat(Enum):
        QOperator = "QOperator"
        QDQ = "QDQ"

    class QuantizationMode(Enum):
        QLinearOps = "QLinearOps"
        IntegerOps = "IntegerOps"

    class QuantType(Enum):
        QUInt8 = "QUInt8"
        QInt8 = "QInt8"
        QUInt16 = "QUInt16"
        QInt16 = "QInt16"


@dataclass
class QuantizationConfig:
    """QuantizationConfig is the configuration class handling all the ONNX Runtime quantization parameters.

    Args:
        is_static (bool):
            Whether to apply static quantization or dynamic quantization.
        format (QuantFormat):
            Targeted ONNX Runtime quantization representation format.
            For the Operator Oriented (QOperator) format, all the quantized operators have their own ONNX definitions.
            For the Tensor Oriented (QDQ) format, the model is quantized by inserting QuantizeLinear / DeQuantizeLinear
            operators.
        mode (QuantizationMode, defaults to QuantizationMode.QLinearOps):
            Targeted ONNX Runtime quantization mode, default is QLinearOps to match QDQ format.
            When targeting dynamic quantization mode, the default value is `QuantizationMode.IntegerOps` whereas the
            default value for static quantization mode is `QuantizationMode.QLinearOps`.
        activations_dtype (QuantType, defaults to QuantType.QUInt8):
            The quantization data types to use for the activations.
        activations_symmetric (bool, defaults to False):
            Whether to apply symmetric quantization on the activations.
        weights_dtype (QuantType, defaults to QuantType.QInt8):
            The quantization data types to use for the weights.
        weights_symmetric (bool, defaults to True):
            Whether to apply symmetric quantization on the weights.
        per_channel (bool, defaults to False):
            Whether we should quantize per-channel (also known as "per-row"). Enabling this can increase overall
            accuracy while making the quantized model heavier.
        reduce_range (bool, defaults to False):
            Whether to use reduce-range 7-bits integers instead of 8-bits integers.
        nodes_to_quantize (List[str], defaults to []):
            List of the nodes names to quantize. When unspecified, all nodes will be quantized. If empty, all nodes being operators from `operators_to_quantize` will be quantized.
        nodes_to_exclude (List[str], defaults to []):
            List of the nodes names to exclude when applying quantization. The list of nodes in a model can be found loading the ONNX model through onnx.load, or through visual inspection with [netron](https://github.com/lutzroeder/netron).
        operators_to_quantize (List[str]):
            List of the operators types to quantize. Defaults to all quantizable operators for the given quantization mode and format. Quantizable operators can be found at https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/tools/quantization/registry.py.
        qdq_add_pair_to_weight (bool, defaults to False):
            By default, floating-point weights are quantized and feed to solely inserted DeQuantizeLinear node.
            If set to True, the floating-point weights will remain and both QuantizeLinear / DeQuantizeLinear nodes
            will be inserted.
        qdq_dedicated_pair (bool, defaults to False):
            When inserting QDQ pair, multiple nodes can share a single QDQ pair as their inputs. If True, it will
            create an identical and dedicated QDQ pair for each node.
        qdq_op_type_per_channel_support_to_axis (Dict[str, int]):
            Set the channel axis for a specific operator type. Effective only when per channel quantization is
            supported and `per_channel` is set to True.
    """

    is_static: bool
    format: QuantFormat
    mode: QuantizationMode = QuantizationMode.QLinearOps
    activations_dtype: QuantType = QuantType.QUInt8
    activations_symmetric: bool = False
    weights_dtype: QuantType = QuantType.QInt8
    weights_symmetric: bool = True
    per_channel: bool = False
    reduce_range: bool = False
    nodes_to_quantize: List[str] = field(default_factory=list)
    nodes_to_exclude: List[str] = field(default_factory=list)
    operators_to_quantize: Optional[List[str]] = None
    qdq_add_pair_to_weight: bool = False
    qdq_dedicated_pair: bool = False
    qdq_op_type_per_channel_support_to_axis: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Adjust default mode based on static/dynamic flag
        if self.mode is None:
            self.mode = (
                QuantizationMode.QLinearOps if self.is_static else QuantizationMode.IntegerOps
            )

        # Ensure operators_to_quantize is a list; if None, leave as None (handled elsewhere)
        if self.operators_to_quantize is None:
            self.operators_to_quantize = []

        # Validate that per_channel is only used with supported modes
        if self.per_channel and self.mode == QuantizationMode.IntegerOps:
            raise ValueError(
                "Per-channel quantization is not supported for IntegerOps mode."
            )

        # Validate that reduce_range is only used with 8-bit types
        if self.reduce_range and (
            self.activations_dtype not in {QuantType.QUInt8, QuantType.QInt8}
            or self.weights_dtype not in {QuantType.QUInt8, QuantType.QInt8}
        ):
            raise ValueError(
                "Reduce range is only supported for 8-bit quantization types."
            )

    @staticmethod
    def quantization_type_str(
        activations_dtype: QuantType, weights_dtype: QuantType
    ) -> str:
        """Return a string representation of the quantization types."""
        return f"{activations_dtype.name}_{weights_dtype.name}"

    @property
    def use_symmetric_calibration(self) -> bool:
        """Whether symmetric calibration should be used."""
        return self.activations_symmetric or self.weights_symmetric

    def __str__(self) -> str:
        attrs = (
            f"is_static={self.is_static}",
            f"format={self.format.name}",
            f"mode={self.mode.name}",
            f"activations_dtype={self.activations_dtype.name}",
            f"activations_symmetric={self.activations_symmetric}",
            f"weights_dtype={self.weights_dtype.name}",
            f"weights_symmetric={self.weights_symmetric}",
            f"per_channel={self.per_channel}",
            f"reduce_range={self.reduce_range}",
            f"nodes_to_quantize={self.nodes_to_quantize}",
            f"nodes_to_exclude={self.nodes_to_exclude}",
            f"operators_to_quantize={self.operators_to_quantize}",
            f"qdq_add_pair_to_weight={self.qdq_add_pair_to_weight}",
            f"qdq_dedicated_pair={self.qdq_dedicated_pair}",
            f"qdq_op_type_per_channel_support_to_axis={self.qdq_op_type_per_channel_support_to_axis}",
        )
        return f"QuantizationConfig({', '.join(attrs)})"