class VideoFormat:
    
    formats = ['mp4', 'avi', 'mkv', 'mov']
    
    @classmethod
    def get_formats(cls):
        return cls.formats