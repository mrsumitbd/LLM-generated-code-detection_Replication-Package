import typing

class ExtraPipelineTaskConfig:

    def __init__(self):
        self.descriptor_configs = {}

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        self.descriptor_configs[descriptor] = {"pipe": pipe, "task": task}

    def get_descriptor_config(self, descriptor: int):
        return self.descriptor_configs.get(descriptor)

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        return list(self.descriptor_configs.keys())