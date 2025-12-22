def validate_version(version: str) -> Tuple[bool, str, bool]:
    import re

    pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-(\w+)(\d+))?$'
    match = re.match(pattern, version)

    if match:
        major, minor, patch, pre_release, pre_release_num = match.groups()
        clean_version = f"{major}.{minor}.{patch}"
        is_stable = False if pre_release else True
        return True, clean_version, is_stable
    else:
        return False, "", False