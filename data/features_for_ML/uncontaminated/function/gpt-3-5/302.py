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
    if not variables:
        variables = {}
    variables["secure_file_priv"] = "/"

    pass