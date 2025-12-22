from functools import cached_property

class SchemaRegistryResourceWithStreamingResponse:

    def __init__(self, schema_registry: SchemaRegistryResource) -> None:
        self.schema_registry = schema_registry

    @cached_property
    def config(self) -> ConfigResourceWithStreamingResponse:
        return ConfigResourceWithStreamingResponse()