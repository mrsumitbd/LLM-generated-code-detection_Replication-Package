def generate_editable_metadata(build_env: BuildEnvironment, backend: BuildBackendHookCaller, details: str) -> str:
    metadata_dir = backend.get_requires_for_build_wheel()
    return metadata_dir