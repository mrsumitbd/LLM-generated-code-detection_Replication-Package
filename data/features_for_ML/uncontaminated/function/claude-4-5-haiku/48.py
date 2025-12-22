def get_compressor(name,
                   zarr_format = ZARR_V2,
                   **params):
    """
    Get a compressor instance by name.
    
    Parameters
    ----------
    name : str
        Name of the compressor (e.g., 'blosc', 'zstd', 'gzip', 'bz2')
    zarr_format : int, optional
        Zarr format version (default: ZARR_V2)
    **params : dict
        Additional parameters to pass to the compressor
    
    Returns
    -------
    Compressor instance or None
    """
    import zarr
    from zarr.codecs import Codec
    
    if name is None:
        return None
    
    name_lower = name.lower() if isinstance(name, str) else name
    
    if zarr_format == ZARR_V2:
        # Zarr v2 compressors
        if name_lower == 'blosc':
            from zarr.codecs import Blosc
            return Blosc(**params) if hasattr(zarr, 'Blosc') else zarr.Blosc(**params)
        elif name_lower == 'zstd':
            from zarr.codecs import ZstdCodec
            return ZstdCodec(**params)
        elif name_lower == 'gzip':
            from zarr.codecs import GzipCodec
            return GzipCodec(**params)
        elif name_lower == 'bz2':
            from zarr.codecs import Bz2Codec
            return Bz2Codec(**params)
        elif name_lower == 'lz4':
            try:
                from zarr.codecs import Lz4Codec
                return Lz4Codec(**params)
            except ImportError:
                return None
        else:
            return None
    else:
        # Zarr v3 compressors
        if name_lower == 'blosc':
            from zarr.codecs import BloscCodec
            return BloscCodec(**params)
        elif name_lower == 'zstd':
            from zarr.codecs import ZstdCodec
            return ZstdCodec(**params)
        elif name_lower == 'gzip':
            from zarr.codecs import GzipCodec
            return GzipCodec(**params)
        elif name_lower == 'bz2':
            from zarr.codecs import Bz2Codec
            return Bz2Codec(**params)
        elif name_lower == 'lz4':
            try:
                from zarr.codecs import Lz4Codec
                return Lz4Codec(**params)
            except ImportError:
                return None
        else:
            return None