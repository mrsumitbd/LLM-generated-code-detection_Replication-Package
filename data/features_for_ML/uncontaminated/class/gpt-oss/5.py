import typing
from dataclasses import dataclass, field


class ExtraPipelineTaskConfig:
    @dataclass
    class _DescriptorConfig:
        descriptor: int
        pipe: "PipeType"
        task: "PipelineTask"

    def __init__(self) -> None:
        self._configs: typing.List[ExtraPipelineTaskConfig._DescriptorConfig] = []

    def add_descriptor(self, descriptor: int, pipe: "PipeType", task: "PipelineTask") -> None:
        """
        Add a new descriptor configuration. If a configuration with the same descriptor
        already exists, it will be replaced.
        """
        # Remove any existing config with the same descriptor
        self._configs = [c for c in self._configs if c.descriptor != descriptor]
        # Append the new configuration
        self._configs.append(self._DescriptorConfig(descriptor, pipe, task))

    def get_descriptor_config(self, descriptor: int) -> typing.Optional["_DescriptorConfig"]:
        """
        Retrieve the configuration for the given descriptor, or None if not found.
        """
        for cfg in self._configs:
            if cfg.descriptor == descriptor:
                return cfg
        return None

    def get_descriptors(self) -> typing.List["_DescriptorConfig"]:
        """
        Return a list of all descriptor configurations.
        """
        return list(self._configs)