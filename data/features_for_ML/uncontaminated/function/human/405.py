def _set_osft_dtypes(model, osft_upcast_dtype, osft_output_dtype):
    """
    Set OSFT dtype attributes on model for computation precision control.
    
    Args:
        model: The OSFT model to configure
        osft_upcast_dtype: Upcast dtype for computations
        osft_output_dtype: Output dtype for results
    """
    model.upcast_dtype = osft_upcast_dtype
    if osft_output_dtype:
        model.output_dtype = osft_output_dtype