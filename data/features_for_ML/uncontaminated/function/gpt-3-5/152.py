def protected_resource_metadata(request: Request, auth_service: AuthServiceDependency, resource: str = ""):
    if not auth_service.is_authorized(request):
        raise UnauthorizedError("User is not authorized to access the resource")
    
    metadata = auth_service.get_resource_metadata(resource)
    return metadata