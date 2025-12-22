from typing import Dict, Any

def create_tenant(
    zone_replica_type: Dict[str, str],
    memory_size: str = "2G",
    cpu_count: int = 1,
    unit_num: int = 1,
    log_disk_size: str = "",
    mode: str = "MYSQL",
    primary_zone: str = "RANDOM",
    whitelist: str = "%",
    scenario: str = None,
    import_script: bool = False,
    charset: str = None,
    collation: str = None,
    read_only: bool = False,
    comment: str = None,
    variables: dict = None,
    parameters: dict = None,
) -> Dict[str, Any]:
    """
    Construct a tenant configuration dictionary.

    Parameters
    ----------
    zone_replica_type : Dict[str, str]
        Mapping of zone names to replica types.
    memory_size : str, optional
        Memory size for the tenant, default "2G".
    cpu_count : int, optional
        Number of CPUs, default 1.
    unit_num : int, optional
        Unit number, default 1.
    log_disk_size : str, optional
        Size of the log disk, default "".
    mode : str, optional
        Mode of the tenant, default "MYSQL".
    primary_zone : str, optional
        Primary zone, default "RANDOM".
    whitelist : str, optional
        Whitelist string, default "%".
    scenario : str, optional
        Scenario name.
    import_script : bool, optional
        Whether to import script, default False.
    charset : str, optional
        Character set.
    collation : str, optional
        Collation.
    read_only : bool, optional
        Read-only flag, default False.
    comment : str, optional
        Comment string.
    variables : dict, optional
        Additional variables.
    parameters : dict, optional
        Additional parameters.

    Returns
    -------
    Dict[str, Any]
        Dictionary representing the tenant configuration.
    """
    # Ensure variables dict exists
    if variables is None:
        variables = {}
    # Set secure_file_priv early
    variables["secure_file_priv"] = "/"

    # Build the tenant configuration
    tenant = {
        "zone_replica_type": zone_replica_type,
        "memory_size": memory_size,
        "cpu_count": cpu_count,
        "unit_num": unit_num,
        "log_disk_size": log_disk_size,
        "mode": mode,
        "primary_zone": primary_zone,
        "whitelist": whitelist,
        "scenario": scenario,
        "import_script": import_script,
        "charset": charset,
        "collation": collation,
        "read_only": read_only,
        "comment": comment,
        "variables": variables,
        "parameters": parameters,
    }

    # Remove keys with None values for cleanliness
    cleaned_tenant = {k: v for k, v in tenant.items() if v is not None}

    return cleaned_tenant