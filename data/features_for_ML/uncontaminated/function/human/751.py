from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

def api_docs_put(item: str) -> dict:
    return {
        200: OpenApiResponse(response=GenericItemResponse, description=f'{item} updated'),
        400: OpenApiResponse(response=GenericErrorResponse, description=f'Invalid {item} data provided'),
        403: OpenApiResponse(response=GenericErrorResponse, description=f'Not privileged to edit the {item}'),
        404: OpenApiResponse(response=GenericErrorResponse, description=f'{item} does not exist'),
    }