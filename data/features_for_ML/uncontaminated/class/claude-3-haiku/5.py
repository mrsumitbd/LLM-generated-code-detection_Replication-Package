import typing

class _DescriptorConfig:
    def __init__(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        self.descriptor = descriptor
        self.pipe = pipe
        self.task = task

class ExtraPipelineTaskConfig:
    def __init__(self):
        self._descriptor_configs = {}

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        descriptor_config = _DescriptorConfig(descriptor, pipe, task)
        self._descriptor_configs[descriptor] = descriptor_config

    def get_descriptor_config(self, descriptor: int) -> "_DescriptorConfig":
        return self._descriptor_configs.get(descriptor, None)

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        return list(self._descriptor_configs.values())