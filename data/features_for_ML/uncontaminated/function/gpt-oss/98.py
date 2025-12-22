def from_codecs(codecs: str) -> Video.Codec:
    """
    Convert a codec string to a Video.Codec enum value.

    Parameters
    ----------
    codecs : str
        The codec identifier (e.g., "h264", "hevc", "vp9", "mpeg4", "av1").

    Returns
    -------
    Video.Codec
        The corresponding Video.Codec enum member.

    Raises
    ------
    ValueError
        If the codec string is not recognized.
    """
    # Normalise the input string
    key = codecs.strip().lower()

    # Mapping from string identifiers to Video.Codec enum members
    _codec_map = {
        # H.264 / AVC
        "h264": Video.Codec.H264,
        "avc1": Video.Codec.H264,
        "h.264": Video.Codec.H264,
        "h.264.": Video.Codec.H264,
        # H.265 / HEVC
        "h265": Video.Codec.HEVC,
        "hevc": Video.Codec.HEVC,
        "h.265": Video.Codec.HEVC,
        # VP9
        "vp9": Video.Codec.VP9,
        # MPEG-4 Part 2
        "mpeg4": Video.Codec.MPEG4,
        "mp4v": Video.Codec.MPEG4,
        # AV1
        "av1": Video.Codec.AV1,
        # Add more aliases if needed
    }

    try:
        return _codec_map[key]
    except KeyError:
        raise ValueError(f"Unsupported codec: {codecs!r}") from None