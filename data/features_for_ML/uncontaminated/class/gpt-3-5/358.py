from typing import List, Dict

class QuantizationConfig:
    def __init__(self, is_static: bool, format: QuantFormat, mode: QuantizationMode = QuantizationMode.QLinearOps,
                 activations_dtype: QuantType = QuantType.QUInt8, activations_symmetric: bool = False,
                 weights_dtype: QuantType = QuantType.QInt8, weights_symmetric: bool = True,
                 per_channel: bool = False, reduce_range: bool = False, nodes_to_quantize: List[str] = [],
                 nodes_to_exclude: List[str] = [], operators_to_quantize: List[str] = [],
                 qdq_add_pair_to_weight: bool = False, qdq_dedicated_pair: bool = False,
                 qdq_op_type_per_channel_support_to_axis: Dict[str, int] = {}):
        self.is_static = is_static
        self.format = format
        self.mode = mode
        self.activations_dtype = activations_dtype
        self.activations_symmetric = activations_symmetric
        self.weights_dtype = weights_dtype
        self.weights_symmetric = weights_symmetric
        self.per_channel = per_channel
        self.reduce_range = reduce_range
        self.nodes_to_quantize = nodes_to_quantize
        self.nodes_to_exclude = nodes_to_exclude
        self.operators_to_quantize = operators_to_quantize
        self.qdq_add_pair_to_weight = qdq_add_pair_to_weight
        self.qdq_dedicated_pair = qdq_dedicated_pair
        self.qdq_op_type_per_channel_support_to_axis = qdq_op_type_per_channel_support_to_axis

    @staticmethod
    def quantization_type_str(activations_dtype: QuantType, weights_dtype: QuantType) -> str:
        return f"{activations_dtype.name}_{weights_dtype.name}"

    @property
    def use_symmetric_calibration(self) -> bool:
        return self.activations_symmetric and self.weights_symmetric

    def __str__(self):
        return f"QuantizationConfig(is_static={self.is_static}, format={self.format}, mode={self.mode}, " \
               f"activations_dtype={self.activations_dtype}, activations_symmetric={self.activations_symmetric}, " \
               f"weights_dtype={self.weights_dtype}, weights_symmetric={self.weights_symmetric}, " \
               f"per_channel={self.per_channel}, reduce_range={self.reduce_range}, " \
               f"nodes_to_quantize={self.nodes_to_quantize}, nodes_to_exclude={self.nodes_to_exclude}, " \
               f"operators_to_quantize={self.operators_to_quantize}, qdq_add_pair_to_weight={self.qdq_add_pair_to_weight}, " \
               f"qdq_dedicated_pair={self.qdq_dedicated_pair}, qdq_op_type_per_channel_support_to_axis={self.qdq_op_type_per_channel_support_to_axis})"