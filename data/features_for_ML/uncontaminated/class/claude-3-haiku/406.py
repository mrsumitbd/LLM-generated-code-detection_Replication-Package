import os
from pathlib import Path

class ArcadeGames:
    """
    Game storage and metadata manager.

    This class is intentionally free of LLM logic and process execution logic.
    It only knows where games live on disk, how to persist metadata, and which
    games are built-in.
    """

    def __init__(self):
        self.games_dir = Path("games")
        self.metadata_file = self.games_dir / "metadata.json"
        self.metadata = {}

    def save_metadata(self):
        self.games_dir.mkdir(exist_ok=True)
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f)

    def save_game_file(self, game_id: str, code: str) -> Path:
        game_file = self.games_dir / f"{game_id}.py"
        with open(game_file, "w") as f:
            f.write(code)
        return game_file

    def read_game_file(self, game_id: str) -> str:
        game_file = self.games_dir / f"{game_id}.py"
        with open(game_file, "r") as f:
            return f.read()