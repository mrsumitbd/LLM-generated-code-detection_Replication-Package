def from_codecs(codecs: str) -> Video.Codec:
    if codecs == "h264":
        return Video.Codec.H264
    elif codecs == "vp9":
        return Video.Codec.VP9
    elif codecs == "av1":
        return Video.Codec.AV1
    else:
        return Video.Codec.UNKNOWN