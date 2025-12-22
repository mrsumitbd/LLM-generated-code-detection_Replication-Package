from typing import Any, Dict, List, Optional

def get_installation_info() -> Dict[str, Dict[str, Any]]:
    libraries = _build_config_snapshot()
    return {
        name: {
            "package": lib.package_name,
            "import": lib.import_path,
            "description": lib.description,
            "is_builtin": lib.is_builtin,
            "post_install": lib.post_install_commands[0] if lib.post_install_commands else None,
        }
        for name, lib in libraries.items()
    }