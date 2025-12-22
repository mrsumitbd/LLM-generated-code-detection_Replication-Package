from zarr import ZARR_V2, ZARR_V3

def get_compressor(name, zarr_format=ZARR_V2, **params):
    if zarr_format == ZARR_V2:
        if name == 'blosc':
            from numcodecs import Blosc
            return Blosc(**params)
        elif name == 'zlib':
            from numcodecs import Zlib
            return Zlib(**params)
        elif name == 'lz4':
            from numcodecs import LZ4
            return LZ4(**params)
        elif name == 'zstd':
            from numcodecs import Zstd
            return Zstd(**params)
        else:
            raise ValueError(f"Unknown compressor: {name}")
    elif zarr_format == ZARR_V3:
        if name == 'blosc':
            from numcodecs import Blosc
            return Blosc(**params)
        elif name == 'zlib':
            from numcodecs import Zlib
            return Zlib(**params)
        elif name == 'lz4':
            from numcodecs import LZ4
            return LZ4(**params)
        elif name == 'zstd':
            from numcodecs import Zstd
            return Zstd(**params)
        else:
            raise ValueError(f"Unknown compressor: {name}")
    else:
        raise ValueError(f"Unknown Zarr format: {zarr_format}")