class MusicPlayer:
    
    def __init__(self):
        self.playlist = []
        self.current_song = None

    def add_song(self, song):
        self.playlist.append(song)

    def play(self, song):
        if song in self.playlist:
            self.current_song = song
            print(f'Playing {song}')
        else:
            print(f'{song} is not in the playlist')

    def stop(self):
        if self.current_song:
            print(f'Stopping {self.current_song}')
            self.current_song = None
        else:
            print('No song is currently playing')