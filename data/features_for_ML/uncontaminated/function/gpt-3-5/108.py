def update_cargo_toml(file_path: Path, version: str) -> tuple[bool, str, str]:
    import re

    with open(file_path, 'r') as file:
        content = file.read()

    old_version = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content).group(1)

    new_content = re.sub(r'version\s*=\s*["\'][^"\']+["\']', f'version = "{version}"', content)

    with open(file_path, 'w') as file:
        file.write(new_content)

    return old_version != version, old_version, version