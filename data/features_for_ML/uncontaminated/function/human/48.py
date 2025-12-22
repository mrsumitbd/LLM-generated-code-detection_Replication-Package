from zarr import codecs
import zarr, dask, numcodecs

def get_compressor(name,
                   zarr_format = ZARR_V2,
                   **params): ### TODO: continue this, add for zarr3
    name = name.lower()
    assert zarr_format in (ZARR_V2, ZARR_V3)
    compression_dict2 = {
        "blosc": "Blosc",
        "bz2": "BZ2",
        "gzip": "GZip",
        "lzma": "LZMA",
        "lz4": "LZ4",
        "pcodec": "PCodec",
        "zfpy": "ZFPY",
        "zlib": "Zlib",
        "zstd": "Zstd"
    }

    compression_dict3 = {
        "blosc": "BloscCodec",
        "gzip": "GzipCodec",
        "sharding": "ShardingCodec",
        "zstd": "ZstdCodec",
        "crc32ccodec": "CRC32CCodec"
    }

    if zarr_format == ZARR_V2:
        compressor_name = compression_dict2[name]
        compressor_instance = getattr(numcodecs, compressor_name)
    elif zarr_format == ZARR_V3:
        compressor_name = compression_dict3[name]
        compressor_instance = getattr(codecs, compressor_name)
    else:
        raise Exception("Unsupported Zarr format")
    compressor = compressor_instance(**params)
    return compressor