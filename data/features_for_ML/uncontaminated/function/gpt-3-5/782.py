from typing import Dict, Optional

def modify_server_properties(
    server_name: str,
    properties_to_update: Dict[str, str],
    restart_after_modify: bool = False,
    app_context: Optional[AppContext] = None,
) -> Dict[str, str]:
    pass