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

    def __init__(
        self,
        is_static: bool,
        format,
        mode=None,
        activations_dtype=None,
        activations_symmetric: bool = False,
        weights_dtype=None,
        weights_symmetric: bool = True,
        per_channel: bool = False,
        reduce_range: bool = False,
        nodes_to_quantize=None,
        nodes_to_exclude=None,
        operators_to_quantize=None,
        qdq_add_pair_to_weight: bool = False,
        qdq_dedicated_pair: bool = False,
        qdq_op_type_per_channel_support_to_axis=None,
    ):
        self.is_static = is_static
        self.format = format
        self.mode = mode
        self.activations_dtype = activations_dtype
        self.activations_symmetric = activations_symmetric
        self.weights_dtype = weights_dtype
        self.weights_symmetric = weights_symmetric
        self.per_channel = per_channel
        self.reduce_range = reduce_range
        self.nodes_to_quantize = nodes_to_quantize if nodes_to_quantize is not None else []
        self.nodes_to_exclude = nodes_to_exclude if nodes_to_exclude is not None else []
        self.operators_to_quantize = operators_to_quantize if operators_to_quantize is not None else []
        self.qdq_add_pair_to_weight = qdq_add_pair_to_weight
        self.qdq_dedicated_pair = qdq_dedicated_pair
        self.qdq_op_type_per_channel_support_to_axis = (
            qdq_op_type_per_channel_support_to_axis
            if qdq_op_type_per_channel_support_to_axis is not None
            else {}
        )

    def __post_init__(self):
        pass

    @staticmethod
    def quantization_type_str(activations_dtype, weights_dtype) -> str:
        return f"{activations_dtype}_{weights_dtype}"

    @property
    def use_symmetric_calibration(self) -> bool:
        return self.activations_symmetric and self.weights_symmetric

    def __str__(self):
        return (
            f"QuantizationConfig("
            f"is_static={self.is_static}, "
            f"format={self.format}, "
            f"mode={self.mode}, "
            f"activations_dtype={self.activations_dtype}, "
            f"activations_symmetric={self.activations_symmetric}, "
            f"weights_dtype={self.weights_dtype}, "
            f"weights_symmetric={self.weights_symmetric}, "
            f"per_channel={self.per_channel}, "
            f"reduce_range={self.reduce_range}, "
            f"nodes_to_quantize={self.nodes_to_quantize}, "
            f"nodes_to_exclude={self.nodes_to_exclude}, "
            f"operators_to_quantize={self.operators_to_quantize}, "
            f"qdq_add_pair_to_weight={self.qdq_add_pair_to_weight}, "
            f"qdq_dedicated_pair={self.qdq_dedicated_pair}, "
            f"qdq_op_type_per_channel_support_to_axis={self.qdq_op_type_per_channel_support_to_axis}"
            f")"
        )