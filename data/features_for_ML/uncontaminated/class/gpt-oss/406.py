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
        # Base directory for all arcade data
        self.base_dir: Path = Path.home() / ".arcade_games"
        self.games_dir: Path = self.base_dir / "games"
        self.metadata_path: Path = self.base_dir / "metadata.json"

        # Ensure directories exist
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.games_dir.mkdir(parents=True, exist_ok=True)

        # Load existing metadata or start fresh
        if self.metadata_path.is_file():
            with self.metadata_path.open("r", encoding="utf-8") as f:
                self.metadata: Dict[str, Dict[str, Any]] = json.load(f)
        else:
            self.metadata = {}

        # Built‑in games are identified by a flag in the metadata
        # (empty set by default; can be extended by subclasses or external code)
        self.built_in_games = {k for k, v in self.metadata.items() if v.get("built_in")}

    def save_metadata(self) -> None:
        """Persist the current metadata dictionary to disk."""
        with self.metadata_path.open("w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, sort_keys=True)

    def save_game_file(self, game_id: str, code: str) -> Path:
        """
        Save the provided code string to a file associated with `game_id`.

        Parameters
        ----------
        game_id : str
            Identifier for the game. Must be a valid filename component.
        code : str
            Source code or script content to be stored.

        Returns
        -------
        Path
            Absolute path to the saved game file.
        """
        # Sanitize game_id to avoid directory traversal
        safe_id = Path(game_id).stem
        file_path = self.games_dir / f"{safe_id}.txt"

        # Write the code to disk
        with file_path.open("w", encoding="utf-8") as f:
            f.write(code)

        # Update metadata
        self.metadata[safe_id] = {
            "filename": file_path.name,
            "built_in": False,
        }
        self.save_metadata()
        return file_path

    def read_game_file(self, game_id: str) -> str:
        """
        Retrieve the source code for the specified game.

        Parameters
        ----------
        game_id : str
            Identifier for the game.

        Returns
        -------
        str
            The source code content of the game file.

        Raises
        ------
        KeyError
            If the game_id is not known.
        FileNotFoundError
            If the game file does not exist on disk.
        """
        safe_id = Path(game_id).stem
        if safe_id not in self.metadata:
            raise KeyError(f"Unknown game_id: {game_id}")

        meta = self.metadata[safe_id]
        if meta.get("built_in"):
            # Built‑in games are not stored in the games directory.
            # For this generic implementation we simply return an empty string.
            # Subclasses may override this method to provide actual built‑in code.
            return ""

        file_path = self.games_dir / meta["filename"]
        if not file_path.is_file():
            raise FileNotFoundError(f"Game file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            return f.read()