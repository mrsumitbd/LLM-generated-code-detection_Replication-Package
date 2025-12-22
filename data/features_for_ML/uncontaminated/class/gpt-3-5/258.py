from typing import List, Dict, Union, Optional, Tuple
from datetime import datetime

class GitAttributionTracker:
    """Tracks attribution information for code symbols based on git history."""

    def __init__(self, codebase: Codebase, ai_authors: Optional[List[str]] = None):
        self.codebase = codebase
        self.ai_authors = ai_authors
        self.history_built = False
        self.symbol_history_map = {}
        self.symbol_last_editor_map = {}
        self.ai_contribution_stats = {}
        self.ai_touched_symbols = []
        self.ai_contribution_timeline = []

    def build_history(self, max_commits: Optional[int] = None) -> None:
        pass

    def _process_commit(self, commit, diff) -> None:
        pass

    def _process_symbol_location_state(self, filepaths: List[str]):
        pass

    def _get_symbols_affected_by_patch(self, patch, filepath):
        pass

    def _is_tracked_file(self, file_path: str) -> bool:
        pass

    def _ensure_history_built(self) -> None:
        pass

    def map_symbols_to_history(self, force=False) -> None:
        pass

    def get_symbol_history(self, symbol) -> List[Dict]:
        pass

    def get_symbol_last_editor(self, symbol) -> Union[str, None]:
        pass

    def get_ai_contribution_stats(self) -> Dict:
        pass

    def get_ai_touched_symbols(self) -> List[Symbol]:
        pass

    def get_ai_contribution_timeline(self) -> List[Tuple[datetime, int]]:
        pass