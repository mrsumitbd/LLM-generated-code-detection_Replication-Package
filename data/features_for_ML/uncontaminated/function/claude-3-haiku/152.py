def protected_resource_metadata(
    request: Request,
    auth_service: AuthServiceDependency,
    resource: str = "",
):
    """
    Retrieves the metadata for a protected resource.

    Args:
        request (Request): The incoming request object.
        auth_service (AuthServiceDependency): The authentication service dependency.
        resource (str, optional): The identifier of the protected resource. Defaults to an empty string.

    Returns:
        dict: The metadata for the protected resource.
    """
    # Authenticate the user
    user = auth_service.authenticate_user(request)

    # Check if the user has access to the protected resource
    if not auth_service.has_access(user, resource):
        raise PermissionDeniedError("User does not have access to the protected resource.")

    # Fetch the metadata for the protected resource
    metadata = fetch_protected_resource_metadata(resource)

    return metadata