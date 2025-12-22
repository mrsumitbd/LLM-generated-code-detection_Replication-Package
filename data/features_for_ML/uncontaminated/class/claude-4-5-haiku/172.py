class ExtraPipelineTaskConfig:
    def __init__(self):
        self._descriptors = {}

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        self._descriptors[descriptor] = {
            'pipe': pipe,
            'task': task
        }

    def get_descriptor_config(self, descriptor: int):
        return self._descriptors.get(descriptor)

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        return list(self._descriptors.values())