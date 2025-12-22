class VideoFormat:
    _formats = {
        "mp4": "MPEG-4",
        "avi": "AVI",
        "mkv": "Matroska",
        "mov": "QuickTime",
        "flv": "Flash Video",
        "webm": "WebM"
    }

    @classmethod
    def get_formats(cls):
        return cls._formats