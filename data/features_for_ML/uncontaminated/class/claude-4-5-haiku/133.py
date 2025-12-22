import dataclasses
from typing import Optional


@dataclasses.dataclass
class OnnxExportArguments:
    """Arguments to decide how the ModelProto will be saved."""
    
    opset_version: int = dataclasses.field(
        default=14,
        metadata={"help": "The version of the default (ai.onnx) opset to target. Must be >= 11."}
    )
    
    use_external_data_format: bool = dataclasses.field(
        default=False,
        metadata={"help": "Whether to use external data format for the ONNX model."}
    )
    
    save_with_external_data: bool = dataclasses.field(
        default=False,
        metadata={"help": "Whether to save the model with external data."}
    )
    
    external_data_location: Optional[str] = dataclasses.field(
        default=None,
        metadata={"help": "The location to save external data files."}
    )
    
    optimize_model_with_onnxruntime: bool = dataclasses.field(
        default=False,
        metadata={"help": "Whether to optimize the model with ONNX Runtime."}
    )
    
    optimize_with_onnxruntime_by_fusion: bool = dataclasses.field(
        default=False,
        metadata={"help": "Whether to optimize the model with ONNX Runtime by fusion."}
    )
    
    optimize_model_with_onnxruntime_gpu: bool = dataclasses.field(
        default=False,
        metadata={"help": "Whether to optimize the model with ONNX Runtime for GPU."}
    )