def _get_gateway_id(
    tenant: Tenant, gateway_name: str, raise_error: bool = True
) -> Optional[str]:
    try:
        gateway = next(
            (g for g in tenant.gateways if g.name.lower() == gateway_name.lower()), None
        )
        if gateway:
            return gateway.id
        if raise_error:
            raise ValueError(f"Gateway '{gateway_name}' not found for tenant '{tenant.name}'.")
        return None
    except Exception as e:
        if raise_error:
            raise e
        return None