import typing
from dataclasses import dataclass, field

class ExtraPipelineTaskConfig:
    number_of_retries: int = field(init=True, default=None)
    _descriptors: typing.Dict[int, _DescriptorConfig] = field(
        init=False, repr=False, default_factory=dict
    )

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        if 1 < descriptor < 10:
            self._descriptors[descriptor] = _DescriptorConfig(
                pipe=pipe, task=task, descriptor=descriptor
            )
            return True
        return False

    def get_descriptor_config(self, descriptor: int):
        return self._descriptors.get(descriptor)

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        return list(self._descriptors.values())