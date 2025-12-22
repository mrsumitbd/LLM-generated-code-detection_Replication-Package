from functools import cached_property

class ModelsResourceWithRawResponse:

    def __init__(self, models: ModelsResource) -> None:
        self.models = models

    @cached_property
    def providers(self) -> ProvidersResourceWithRawResponse:
        return ProvidersResourceWithRawResponse(self.models.providers)