from pathlib import Path

class ArcadeGames:
    """
    Game storage and metadata manager.

    This class is intentionally free of LLM logic and process execution logic.
    It only knows where games live on disk, how to persist metadata, and which
    games are built-in.
    """

    def __init__(self):
        self.games_metadata = {}

    def save_metadata(self):
        # Implementation to save metadata to disk
        pass

    def save_game_file(self, game_id: str, code: str) -> Path:
        game_file_path = Path(f'games/{game_id}.txt')
        with open(game_file_path, 'w') as file:
            file.write(code)
        return game_file_path

    def read_game_file(self, game_id: str) -> str:
        game_file_path = Path(f'games/{game_id}.txt')
        with open(game_file_path, 'r') as file:
            code = file.read()
        return code