from typing import Dict, Any
from obshell.model.tenant import ZoneParam
import time

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
    # Global variable `secure_file_priv` take a while to take effect, so we set it early (right after tenant creation)
    # if not variables:
    #     variables = {}
    # variables["secure_file_priv"] = "/"

    root_password = SYS_PASSWORD
    global client
    if client is None:
        connect()

    # 创建一个新的 unit config
    unit_config_name = f"{TENANT_NAME}_unit_config_{int(time.time())}"
    client.v1.create_resource_unit_config(
        unit_config_name,
        memory_size,
        cpu_count,
        log_disk_size=(None if log_disk_size == "" else log_disk_size),
    )

    zone_list = [
        ZoneParam(zone, unit_config_name, unit_num, zone_replica_type.get(zone, "FULL"))
        for zone in zone_replica_type
    ]
    return client.v1.create_tenant_sync(
        TENANT_NAME,
        zone_list,
        mode,
        primary_zone,
        whitelist,
        root_password,
        scenario,
        import_script,
        charset,
        collation,
        read_only,
        comment,
        variables,
        parameters,
    )