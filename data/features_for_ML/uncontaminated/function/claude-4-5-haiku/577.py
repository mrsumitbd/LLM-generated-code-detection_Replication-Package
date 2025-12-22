def generate_editable_metadata(
    build_env: BuildEnvironment, backend: BuildBackendHookCaller, details: str
) -> str:
    """Generate metadata using mechanisms described in PEP 660.

    Returns the generated metadata directory.
    """
    import tempfile
    import os
    from pathlib import Path
    
    # Create a temporary directory for the metadata
    metadata_dir = tempfile.mkdtemp(prefix="editable_metadata_")
    
    try:
        # Call the backend hook to prepare metadata for editable install
        # This follows PEP 660 which defines prepare_metadata_for_build_editable hook
        hook_name = "prepare_metadata_for_build_editable"
        
        # Check if the backend supports the editable metadata hook
        if hasattr(backend, hook_name):
            # Call the hook with the metadata directory
            backend_metadata_dir = getattr(backend, hook_name)(metadata_dir, details)
            
            if backend_metadata_dir:
                return backend_metadata_dir
        
        # Fallback: use the standard prepare_metadata_for_build_wheel if available
        if hasattr(backend, "prepare_metadata_for_build_wheel"):
            backend_metadata_dir = backend.prepare_metadata_for_build_wheel(metadata_dir, details)
            if backend_metadata_dir:
                return backend_metadata_dir
        
        # If no metadata preparation hook is available, return the temp directory
        return metadata_dir
        
    except Exception:
        # Clean up on error
        import shutil
        if os.path.exists(metadata_dir):
            shutil.rmtree(metadata_dir, ignore_errors=True)
        raise