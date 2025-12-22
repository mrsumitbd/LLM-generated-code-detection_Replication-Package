from cached_property import cached_property
from .providers import ProvidersResourceWithRawResponse
from .models import ModelsResource

class ModelsResourceWithRawResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

    @cached_property
    def providers(self) -> ProvidersResourceWithRawResponse:
        return ProvidersResourceWithRawResponse(self._models.providers)