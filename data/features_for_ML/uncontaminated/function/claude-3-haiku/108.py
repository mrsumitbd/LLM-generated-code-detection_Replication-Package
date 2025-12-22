from pathlib import Path
import toml

def update_cargo_toml(file_path: Path, version: str) -> tuple[bool, str, str]:
    """
    Update a Cargo.toml file that has hardcoded version (not using workspace).

    Returns: (changed, old_version, new_version)
    """
    try:
        with file_path.open('r') as f:
            cargo_toml = toml.load(f)

        old_version = cargo_toml['package']['version']
        if old_version != version:
            cargo_toml['package']['version'] = version
            with file_path.open('w') as f:
                toml.dump(cargo_toml, f)
            return True, old_version, version
        else:
            return False, old_version, version
    except (FileNotFoundError, KeyError, toml.TomlDecodeError):
        return False, '', version