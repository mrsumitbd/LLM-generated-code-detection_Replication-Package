def _set_osft_dtypes(model, osft_upcast_dtype, osft_output_dtype):
    model.osft_upcast_dtype = osft_upcast_dtype
    model.osft_output_dtype = osft_output_dtype