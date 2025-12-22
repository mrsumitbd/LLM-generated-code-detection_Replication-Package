def check_if_cuda_home_none(global_option: str) -> None:
    """
    Verify that the CUDA_HOME path is provided.

    Parameters
    ----------
    global_option : str
        The value of the CUDA_HOME environment variable or equivalent.

    Raises
    ------
    ValueError
        If `global_option` is None, an empty string, or contains only whitespace.
    """
    # Allow callers to pass None even though the type hint says str
    if global_option is None or not isinstance(global_option, str) or not global_option.strip():
        raise ValueError(
            "CUDA_HOME is not set. Please set the CUDA_HOME environment variable "
            "to the root of your CUDA installation."
        )