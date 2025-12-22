from cached_property import cached_property
from .config import ConfigResourceWithStreamingResponse
from .schema_registry import SchemaRegistryResource

class SchemaRegistryResourceWithStreamingResponse:
    def __init__(self, schema_registry: SchemaRegistryResource) -> None:
        self._schema_registry = schema_registry

    @cached_property
    def config(self) -> ConfigResourceWithStreamingResponse:
        return ConfigResourceWithStreamingResponse(self._schema_registry)