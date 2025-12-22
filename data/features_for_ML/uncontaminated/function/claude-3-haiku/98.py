from enum import Enum

class Video:
    class Codec(Enum):
        H264 = "h264"
        VP9 = "vp9"
        AV1 = "av1"

def from_codecs(codecs: str) -> Video.Codec:
    codec_map = {
        "h264": Video.Codec.H264,
        "avc": Video.Codec.H264,
        "vp9": Video.Codec.VP9,
        "av1": Video.Codec.AV1,
    }
    
    for codec in codecs.split(","):
        codec = codec.strip().lower()
        if codec in codec_map:
            return codec_map[codec]
    
    raise ValueError(f"Invalid codec: {codecs}")