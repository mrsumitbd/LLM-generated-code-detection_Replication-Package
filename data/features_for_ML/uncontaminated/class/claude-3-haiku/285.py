class AudioMetadata:
    """Complete metadata for an audio recording."""

    def __init__(self, title, artist, album, track_number, duration):
        self.title = title
        self.artist = artist
        self.album = album
        self.track_number = track_number
        self.duration = duration

    def __str__(self):
        return f"{self.title} by {self.artist} from the album {self.album} (track {self.track_number}, {self.duration} seconds)"

    def __eq__(self, other):
        return (self.title, self.artist, self.album, self.track_number, self.duration) == (other.title, other.artist, other.album, other.track_number, other.duration)

    def __hash__(self):
        return hash((self.title, self.artist, self.album, self.track_number, self.duration))