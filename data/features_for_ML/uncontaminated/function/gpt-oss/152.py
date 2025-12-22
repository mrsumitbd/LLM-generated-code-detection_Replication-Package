from fastapi import HTTPException, status

def protected_resource_metadata(
    request: Request,
    auth_service: AuthServiceDependency,
    resource: str = "",
):
    """
    Retrieve metadata for a protected resource.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    auth_service : AuthServiceDependency
        Dependency providing authentication and resource lookup.
    resource : str, optional
        The identifier of the resource whose metadata is requested.

    Returns
    -------
    dict
        The metadata dictionary for the requested resource.

    Raises
    ------
    HTTPException
        If the resource is not specified, not found, or the caller is not
        authorized to access it.
    """
    # Ensure a resource identifier was supplied
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource identifier must be provided",
        )

    # Attempt to fetch the metadata from the auth service
    try:
        metadata = auth_service.get_resource_metadata(resource)
    except Exception as exc:
        # Any unexpected exception from the auth service is treated as a
        # server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving resource metadata: {exc}",
        ) from exc

    # If the auth service indicates the resource does not exist, return 404
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource '{resource}' not found",
        )

    # If the auth service returns a boolean False, treat it as forbidden
    if metadata is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access to resource '{resource}' is forbidden",
        )

    # Successful retrieval – return the metadata
    return metadata