def get_installation_info() -> Dict[str, Dict[str, Any]]:
    installation_info = {
        "python": {
            "version": sys.version,
            "path": sys.executable
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "architecture": platform.architecture()
        }
    }
    return installation_info