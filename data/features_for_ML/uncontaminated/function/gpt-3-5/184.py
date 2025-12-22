def _get_gateway_id(tenant: Tenant, gateway_name: str, raise_error: bool = True) -> Optional[str]:
    if raise_error:
        raise ValueError("Gateway not found")
    else:
        return None