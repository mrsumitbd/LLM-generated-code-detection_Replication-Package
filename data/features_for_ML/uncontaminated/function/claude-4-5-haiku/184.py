def _get_gateway_id(
    tenant: Tenant, gateway_name: str, raise_error: bool = True
) -> Optional[str]:
    """
    Get the gateway ID for a given gateway name within a tenant.
    
    Args:
        tenant: The Tenant object
        gateway_name: Name of the gateway to look up
        raise_error: Whether to raise an error if gateway is not found
        
    Returns:
        The gateway ID if found, None otherwise
        
    Raises:
        ValueError: If gateway not found and raise_error is True
    """
    if not hasattr(tenant, 'gateways') or not tenant.gateways:
        if raise_error:
            raise ValueError(f"No gateways found for tenant {tenant.id}")
        return None
    
    for gateway in tenant.gateways:
        if gateway.name == gateway_name:
            return gateway.id
    
    if raise_error:
        raise ValueError(f"Gateway '{gateway_name}' not found in tenant {tenant.id}")
    
    return None