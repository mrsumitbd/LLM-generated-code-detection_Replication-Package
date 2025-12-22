from fastapi import APIRouter, Request
from agentstack_server.api.auth.utils import create_resource_uri
from agentstack_server.api.dependencies import AuthServiceDependency

def protected_resource_metadata(
    request: Request,
    auth_service: AuthServiceDependency,
    resource: str = "",
):
    return auth_service.protected_resource_metadata(resource=create_resource_uri(request.url.replace(path=resource)))