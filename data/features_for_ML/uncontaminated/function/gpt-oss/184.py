from typing import Optional

def _get_gateway_id(
    tenant: "Tenant",
    gateway_name: str,
    raise_error: bool = True,
) -> Optional[str]:
    """
    Retrieve the gateway ID for a given gateway name from a tenant.

    Parameters
    ----------
    tenant : Tenant
        The tenant object that contains gateway information.
    gateway_name : str
        The name of the gateway to look up.
    raise_error : bool, default True
        If True, raise a ValueError when the gateway cannot be found.
        If False, return None instead.

    Returns
    -------
    Optional[str]
        The gateway ID if found, otherwise None (or raises an error if
        raise_error is True).
    """
    # Try to use a direct lookup method if available
    if hasattr(tenant, "get_gateway_by_name"):
        try:
            gw = tenant.get_gateway_by_name(gateway_name)
            # Assume the returned object has an `id` attribute
            return getattr(gw, "id", None)
        except Exception:
            # Fall back to manual search
            pass

    # Fallback: iterate over a `gateways` attribute if it exists
    gateways = getattr(tenant, "gateways", None)
    if gateways is None:
        # Try to get a list via a method
        if hasattr(tenant, "list_gateways"):
            try:
                gateways = tenant.list_gateways()
            except Exception:
                gateways = None

    if gateways:
        for gw in gateways:
            # Support dict or object with name/id attributes
            name = gw.get("name") if isinstance(gw, dict) else getattr(gw, "name", None)
            if name == gateway_name:
                return gw.get("id") if isinstance(gw, dict) else getattr(gw, "id", None)

    # If we reach here, the gateway was not found
    if raise_error:
        raise ValueError(f"Gateway '{gateway_name}' not found in tenant '{tenant}'.")
    return None