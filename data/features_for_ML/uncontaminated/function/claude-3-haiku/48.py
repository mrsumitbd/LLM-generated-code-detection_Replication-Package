import zarr

def get_compressor(name, zarr_format=zarr.ZARR_FORMAT, **params):
    if name == 'gzip':
        return zarr.GZipCompressor(**params)
    elif name == 'lzma':
        return zarr.LZMACompressor(**params)
    elif name == 'bz2':
        return zarr.BZ2Compressor(**params)
    elif name == 'zlib':
        return zarr.ZlibCompressor(**params)
    elif name == 'blosc':
        return zarr.BloscCompressor(**params)
    elif name == 'lz4':
        return zarr.LZ4Compressor(**params)
    elif name == 'zstd':
        return zarr.ZstdCompressor(**params)
    elif name == 'default':
        if zarr_format == zarr.ZARR_FORMAT:
            return zarr.Blosc()
        elif zarr_format == zarr.ZARR_FORMAT_3:
            return zarr.Zstd()
        else:
            raise ValueError(f"Unsupported Zarr format: {zarr_format}")
    else:
        raise ValueError(f"Unsupported compressor name: {name}")