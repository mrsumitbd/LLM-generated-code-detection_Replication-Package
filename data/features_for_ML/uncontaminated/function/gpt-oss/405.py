def _set_osft_dtypes(model, osft_upcast_dtype, osft_output_dtype):
    """
    Set OSFT dtype attributes on model for computation precision control.

    Args:
        model: The OSFT model to configure
        osft_upcast_dtype: Upcast dtype for computations
        osft_output_dtype: Output dtype for results
    """
    # Store the dtypes on the model for later reference
    setattr(model, "osft_upcast_dtype", osft_upcast_dtype)
    setattr(model, "osft_output_dtype", osft_output_dtype)

    # If the model exposes a `dtype` attribute, set it to the output dtype
    if hasattr(model, "dtype"):
        try:
            model.dtype = osft_output_dtype
        except Exception:
            # Some models may not allow direct assignment; ignore silently
            pass

    # Also expose a generic `upcast_dtype` attribute for consistency
    setattr(model, "upcast_dtype", osft_upcast_dtype)