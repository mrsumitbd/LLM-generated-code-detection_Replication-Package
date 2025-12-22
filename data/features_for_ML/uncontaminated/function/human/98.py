def from_codecs(codecs: str) -> Video.Codec:
            for codec in codecs.lower().split(","):
                codec = codec.strip()
                mime = codec.split(".")[0]
                try:
                    return Video.Codec.from_mime(mime)
                except ValueError:
                    pass
            raise ValueError(f"No MIME types matched any supported Video Codecs in '{codecs}'")