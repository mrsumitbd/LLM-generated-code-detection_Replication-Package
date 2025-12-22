import json
from nat.runtime.loader import get_all_entrypoints_distro_mapping

def dump_distro_mapping(path: str):
    mapping = get_all_entrypoints_distro_mapping()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)