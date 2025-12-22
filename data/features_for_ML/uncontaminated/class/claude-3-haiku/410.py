class MusicPlayer:
    def __init__(self):
        self.current_song = None
        self.playlist = []
        self.is_playing = False

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)

    def play(self):
        if self.playlist:
            self.current_song = self.playlist[0]
            self.playlist.pop(0)
            self.is_playing = True
            print(f"Now playing: {self.current_song}")
        else:
            print("Playlist is empty.")

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            print(f"Paused: {self.current_song}")
        else:
            print("Music is not playing.")

    def resume(self):
        if not self.is_playing:
            self.is_playing = True
            print(f"Resumed: {self.current_song}")
        else:
            print("Music is already playing.")

    def show_playlist(self):
        if self.playlist:
            print("Playlist:")
            for song in self.playlist:
                print(song)
        else:
            print("Playlist is empty.")