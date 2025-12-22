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
):
    if variables is None:
        variables = {}
    if parameters is None:
        parameters = {}
    
    tenant_config = {
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
    
    return tenant_config