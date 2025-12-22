import typing
from dataclasses import dataclass

class ExtraPipelineTaskConfig:
    @dataclass
    class _DescriptorConfig:
        descriptor: int
        pipe: typing.Any
        task: typing.Any

    def __init__(self):
        self._configs: typing.Dict[int, ExtraPipelineTaskConfig._DescriptorConfig] = {}

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask"):
        """Add or replace a descriptor configuration."""
        self._configs[descriptor] = self._DescriptorConfig(descriptor, pipe, task)

    def get_descriptor_config(self, descriptor: int) -> typing.Optional["_DescriptorConfig"]:
        """Return the configuration for the given descriptor, or None if not present."""
        return self._configs.get(descriptor)

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        """Return a list of all descriptor configurations."""
        return list(self._configs.values())