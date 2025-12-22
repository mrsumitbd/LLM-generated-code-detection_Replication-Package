def generate_editable_metadata(
    build_env: BuildEnvironment, backend: BuildBackendHookCaller, details: str
) -> str:
    """Generate metadata using mechanisms described in PEP 660.

    Returns the generated metadata directory.
    """
    metadata_dir = build_env.metadata_directory
    backend.build_editable_metadata(metadata_dir, details)
    return metadata_dir