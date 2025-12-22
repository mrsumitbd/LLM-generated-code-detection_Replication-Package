import json
import os

# Define the target migration version that the system should be at.
TARGET_MIGRATION_VERSION = 2

def _load_current_version() -> int:
    """
    Load the current migration version from a JSON file.
    The file is expected to contain a top‑level key "migration_version".
    If the file does not exist or the key is missing, 0 is returned.
    """
    state_file = "migration_state.json"
    if not os.path.exists(state_file):
        return 0
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return int(data.get("migration_version", 0))
    except (ValueError, json.JSONDecodeError, OSError):
        # If the file is corrupted or unreadable, assume no migration has been applied.
        return 0

def check_if_migration_is_needed() -> bool:
    """
    Determine whether a migration step is required.

    The function compares the current migration version stored in
    `migration_state.json` against the TARGET_MIGRATION_VERSION.
    If the current version is less than the target, migration is needed.

    Returns:
        bool: True if migration is needed, False otherwise.
    """
    current_version = _load_current_version()
    return current_version < TARGET_MIGRATION_VERSION