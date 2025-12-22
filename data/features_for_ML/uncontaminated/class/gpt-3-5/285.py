class AudioMetadata:
    def __init__(self, title, artist, album, duration, genre):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.genre = genre

    def display_metadata(self):
        print(f"Title: {self.title}")
        print(f"Artist: {self.artist}")
        print(f"Album: {self.album}")
        print(f"Duration: {self.duration} seconds")
        print(f"Genre: {self.genre}")

# Example usage:
audio = AudioMetadata("Song Title", "Artist Name", "Album Name", 180, "Pop")
audio.display_metadata()