import os
from pathlib import Path
from typing import Any

def generate_editable_metadata(
    build_env: Any,
    backend: Any,
    details: str,
) -> str:
    """
    Generate metadata using mechanisms described in PEP 660.

    Returns the generated metadata directory.
    """
    # Determine the metadata directory from the build environment.
    # The attribute may be a Path or a string; normalise to a Path.
    metadata_dir = Path(getattr(build_env, "metadata_dir", None))
    if metadata_dir is None:
        raise RuntimeError("BuildEnvironment does not provide a metadata_dir attribute")

    # Ensure the directory exists.
    metadata_dir.mkdir(parents=True, exist_ok=True)

    # Call the backend hook to build the editable metadata.
    # The hook is expected to accept (build_env, metadata_dir, details).
    # It may raise an exception if it fails; we simply propagate it.
    backend.build_editable_metadata(build_env, str(metadata_dir), details)

    # Return the path as a string.
    return str(metadata_dir)