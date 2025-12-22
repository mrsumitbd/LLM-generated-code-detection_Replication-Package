from dataclasses import dataclass, field

class OnnxExportArguments:
    """Arguments to decide how the ModelProto will be saved."""

    use_external_data_format: bool = field(
        default=False,
        metadata={"help": "Whether to use external data format to store model whose size is >= 2Gb."},
    )
    one_external_file: bool = field(
        default=True,
        metadata={"help": "When `use_external_data_format=True`, whether to save all tensors to one external file."},
    )