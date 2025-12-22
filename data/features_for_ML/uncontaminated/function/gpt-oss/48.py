# -*- coding: utf-8 -*-

"""
Utility for obtaining compressor instances for Zarr arrays.
"""

from __future__ import annotations

# Import compressor classes.  The actual module names may vary depending on the
# Zarr version; adjust the imports accordingly.
try:
    # Zarr 2.x
    from zarr.compressor import (
        CompressorBase,
        ZlibCompressor,
        LZ4Compressor,
        BloscCompressor,
        ZstdCompressor,
        NoneCompressor,
    )
except Exception:
    # Fallback for older or custom installations
    from zarr import (
        CompressorBase,
        ZlibCompressor,
        LZ4Compressor,
        BloscCompressor,
        ZstdCompressor,
        NoneCompressor,
    )

# Constants for Zarr format versions
try:
    from zarr.constants import ZARR_V2, ZARR_V3
except Exception:
    # Default values if constants are not available
    ZARR_V2 = 2
    ZARR_V3 = 3


def get_compressor(name,
                   zarr_format: int = ZARR_V2,
                   **params) -> CompressorBase:
    """
    Return a compressor instance based on the supplied name or object.

    Parameters
    ----------
    name : str | CompressorBase | None
        The name of the compressor to use, an existing compressor instance,
        or ``None``/``'none'`` for no compression.
    zarr_format : int, optional
        The Zarr format version.  Currently only used to select the
        appropriate compressor class for Zarr v3; for v2 the mapping is
        identical.
    **params
        Additional keyword arguments passed to the compressor constructor.
        Commonly used for compression level (e.g., ``level=5`` for zlib).

    Returns
    -------
    CompressorBase
        An instance of the requested compressor.

    Raises
    ------
    ValueError
        If an unknown compressor name is supplied.
    TypeError
        If the supplied ``name`` is not a string, compressor instance, or
        ``None``.
    """
    # Handle the "no compression" case
    if name is None or (isinstance(name, str) and name.lower() == "none"):
        return NoneCompressor()

    # If an instance is supplied, just return it
    if isinstance(name, CompressorBase):
        return name

    # If a string is supplied, map it to a compressor class
    if isinstance(name, str):
        name_lc = name.lower()

        # Mapping for Zarr v2 and v3 (currently identical)
        if zarr_format == ZARR_V3:
            # In Zarr v3 the compressor classes are the same as v2,
            # but the API may change in the future.  For now we use the
            # same mapping.
            pass

        if name_lc == "zlib":
            level = params.get("level", 6)
            return ZlibCompressor(level=level)

        if name_lc == "lz4":
            return LZ4Compressor()

        if name_lc == "blosc":
            return BloscCompressor()

        if name_lc == "zstd":
            level = params.get("level", 3)
            return ZstdCompressor(level=level)

        if name_lc == "zstd_fast":
            return ZstdCompressor(level=1)

        if name_lc == "zstd_best":
            return ZstdCompressor(level=22)

        # Add any additional compressor names here as needed

        raise ValueError(f"Unknown compressor name: {name}")

    # Unsupported type
    raise TypeError(
        f"Unsupported compressor type: {type(name).__name__}. "
        "Expected a string, CompressorBase instance, or None."
    )