from dataclasses import asdict, dataclass, field
from onnxruntime.quantization import CalibraterBase, CalibrationMethod, QuantFormat, QuantizationMode, QuantType

class QuantizationConfig:
    """QuantizationConfig is the configuration class handling all the ONNX Runtime quantization parameters.

    Args:
        is_static (`bool`):
            Whether to apply static quantization or dynamic quantization.
        format (`QuantFormat`):
            Targeted ONNX Runtime quantization representation format.
            For the Operator Oriented (QOperator) format, all the quantized operators have their own ONNX definitions.
            For the Tensor Oriented (QDQ) format, the model is quantized by inserting QuantizeLinear / DeQuantizeLinear
            operators.
        mode (`QuantizationMode`, defaults to `QuantizationMode.QLinearOps`):
            Targeted ONNX Runtime quantization mode, default is QLinearOps to match QDQ format.
            When targeting dynamic quantization mode, the default value is `QuantizationMode.IntegerOps` whereas the
            default value for static quantization mode is `QuantizationMode.QLinearOps`.
        activations_dtype (`QuantType`, defaults to `QuantType.QUInt8`):
            The quantization data types to use for the activations.
        activations_symmetric (`bool`, defaults to `False`):
            Whether to apply symmetric quantization on the activations.
        weights_dtype (`QuantType`, defaults to `QuantType.QInt8`):
            The quantization data types to use for the weights.
        weights_symmetric (`bool`, defaults to `True`):
            Whether to apply symmetric quantization on the weights.
        per_channel (`bool`, defaults to `False`):
            Whether we should quantize per-channel (also known as "per-row"). Enabling this can increase overall
            accuracy while making the quantized model heavier.
        reduce_range (`bool`, defaults to `False`):
            Whether to use reduce-range 7-bits integers instead of 8-bits integers.
        nodes_to_quantize (`List[str]`, defaults to `[]`):
            List of the nodes names to quantize. When unspecified, all nodes will be quantized. If empty, all nodes being operators from `operators_to_quantize` will be quantized.
        nodes_to_exclude (`List[str]`, defaults to `[]`):
            List of the nodes names to exclude when applying quantization. The list of nodes in a model can be found loading the ONNX model through onnx.load, or through visual inspection with [netron](https://github.com/lutzroeder/netron).
        operators_to_quantize (`List[str]`):
            List of the operators types to quantize. Defaults to all quantizable operators for the given quantization mode and format. Quantizable operators can be found at https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/tools/quantization/registry.py.
        qdq_add_pair_to_weight (`bool`, defaults to `False`):
            By default, floating-point weights are quantized and feed to solely inserted DeQuantizeLinear node.
            If set to True, the floating-point weights will remain and both QuantizeLinear / DeQuantizeLinear nodes
            will be inserted.
        qdq_dedicated_pair (`bool`, defaults to `False`):
            When inserting QDQ pair, multiple nodes can share a single QDQ pair as their inputs. If True, it will
            create an identical and dedicated QDQ pair for each node.
        qdq_op_type_per_channel_support_to_axis (`Dict[str, int]`):
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
    nodes_to_quantize: list[str] = field(default_factory=list)
    nodes_to_exclude: list[str] = field(default_factory=list)
    operators_to_quantize: list[str] = field(default_factory=list)
    qdq_add_pair_to_weight: bool = False
    qdq_dedicated_pair: bool = False
    qdq_op_type_per_channel_support_to_axis: dict[str, int] = field(
        default_factory=lambda: ORT_DEFAULT_CHANNEL_FOR_OPERATORS
    )

    def __post_init__(self):
        ensure_valid_mode_or_raise(self.is_static, self.mode)
        ensure_valid_data_type_or_raise(self.is_static, self.activations_dtype, self.weights_dtype)

        # If needed, dynamically set operators_to_quantize default.
        if len(self.operators_to_quantize) == 0:
            _, _, operators_to_quantize = default_quantization_parameters(
                self.is_static, self.format, self.mode, self.operators_to_quantize
            )
            self.operators_to_quantize = operators_to_quantize

        if isinstance(self.format, str):
            self.format = QuantFormat[self.format]
        if isinstance(self.mode, str):
            self.mode = QuantizationMode[self.mode]
        if isinstance(self.activations_dtype, str):
            self.activations_dtype = QuantType[self.activations_dtype]
        if isinstance(self.weights_dtype, str):
            self.weights_dtype = QuantType[self.weights_dtype]

    @staticmethod
    def quantization_type_str(activations_dtype: QuantType, weights_dtype: QuantType) -> str:
        return (
            f"{'s8' if activations_dtype == QuantType.QInt8 else 'u8'}"
            f"/"
            f"{'s8' if weights_dtype == QuantType.QInt8 else 'u8'}"
        )

    @property
    def use_symmetric_calibration(self) -> bool:
        return self.activations_symmetric and self.weights_symmetric

    def __str__(self):
        return (
            f"{self.format} ("
            f"mode: {self.mode}, "
            f"schema: {QuantizationConfig.quantization_type_str(self.activations_dtype, self.weights_dtype)}, "
            f"channel-wise: {self.per_channel})"
        )