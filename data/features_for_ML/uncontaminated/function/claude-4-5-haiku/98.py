def from_codecs(codecs: str) -> Video.Codec:
    """Convert a codecs string to a Video.Codec enum value."""
    codecs = codecs.strip().lower()
    
    # Handle common codec strings
    codec_map = {
        'h264': Video.Codec.H264,
        'avc1': Video.Codec.H264,
        'avc': Video.Codec.H264,
        'h265': Video.Codec.H265,
        'hevc': Video.Codec.H265,
        'hev1': Video.Codec.H265,
        'vp8': Video.Codec.VP8,
        'vp9': Video.Codec.VP9,
        'av1': Video.Codec.AV1,
        'mpeg2': Video.Codec.MPEG2,
        'mpeg4': Video.Codec.MPEG4,
        'wmv': Video.Codec.WMV,
        'prores': Video.Codec.PRORES,
        'dnxhd': Video.Codec.DNXHD,
    }
    
    # Check for exact matches first
    if codecs in codec_map:
        return codec_map[codecs]
    
    # Check for partial matches (e.g., "avc1.42e01e" contains "avc1")
    for key, value in codec_map.items():
        if key in codecs:
            return value
    
    # Default fallback
    return Video.Codec.H264