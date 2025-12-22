class OnnxExportArguments:
    """Arguments to decide how the ModelProto will be saved."""

    def __init__(
        self,
        output_path: str,
        opset_version: int = 13,
        use_external_data_format: bool = False,
        strip_doc_string: bool = True,
        keep_initializers_as_inputs: bool = False,
        save_model_format: str = "protobuf",
    ):
        self.output_path = output_path
        self.opset_version = opset_version
        self.use_external_data_format = use_external_data_format
        self.strip_doc_string = strip_doc_string
        self.keep_initializers_as_inputs = keep_initializers_as_inputs
        self.save_model_format = save_model_format