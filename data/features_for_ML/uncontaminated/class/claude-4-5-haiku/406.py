import json
from pathlib import Path
from typing import Dict, Any


class ArcadeGames:
    """
    Game storage and metadata manager.

    This class is intentionally free of LLM logic and process execution logic.
    It only knows where games live on disk, how to persist metadata, and which
    games are built-in.
    """

    def __init__(self):
        self.games_dir = Path.home() / ".arcade_games"
        self.games_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.games_dir / "metadata.json"
        self.metadata: Dict[str, Any] = self._load_metadata()
        self.builtin_games = {
            "pong": "Built-in Pong game",
            "snake": "Built-in Snake game",
            "breakout": "Built-in Breakout game",
        }

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from disk or return empty dict if not exists."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_metadata(self):
        """Persist metadata to disk."""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def save_game_file(self, game_id: str, code: str) -> Path:
        """
        Save game code to disk.
        
        Args:
            game_id: Unique identifier for the game
            code: Python code for the game
            
        Returns:
            Path to the saved game file
        """
        game_file = self.games_dir / f"{game_id}.py"
        with open(game_file, "w") as f:
            f.write(code)
        
        # Update metadata
        self.metadata[game_id] = {
            "filename": game_file.name,
            "path": str(game_file),
            "builtin": False,
        }
        self.save_metadata()
        
        return game_file

    def read_game_file(self, game_id: str) -> str:
        """
        Read game code from disk.
        
        Args:
            game_id: Unique identifier for the game
            
        Returns:
            The game code as a string
            
        Raises:
            FileNotFoundError: If the game file doesn't exist
        """
        if game_id in self.metadata:
            game_path = Path(self.metadata[game_id]["path"])
        else:
            game_path = self.games_dir / f"{game_id}.py"
        
        if not game_path.exists():
            raise FileNotFoundError(f"Game file not found: {game_id}")
        
        with open(game_path, "r") as f:
            return f.read()