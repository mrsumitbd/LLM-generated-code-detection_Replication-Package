from typing import Codebase, Patch, Symbol
from datetime import datetime

class GitAttributionTracker:
    """Tracks attribution information for code symbols based on git history."""

    def __init__(self, codebase: Codebase, ai_authors: list[str] | None = None):
        self.codebase = codebase
        self.ai_authors = ai_authors or []
        self.symbol_history = {}
        self.history_built = False

    def build_history(self, max_commits: int | None = None) -> None:
        self._ensure_history_built()
        for commit, diff in self.codebase.get_commits(max_commits):
            self._process_commit(commit, diff)
        self.history_built = True

    def _process_commit(self, commit, diff) -> None:
        for filepath in diff.get_modified_files():
            if self._is_tracked_file(filepath):
                self._process_symbol_location_state(diff.get_modified_symbols(filepath))

    def _process_symbol_location_state(self, filepaths: list[str]):
        for filepath in filepaths:
            symbols = self.codebase.get_symbols(filepath)
            for symbol in symbols:
                self._update_symbol_history(symbol, filepath)

    def _get_symbols_affected_by_patch(self, patch: Patch, filepath):
        symbols = self.codebase.get_symbols(filepath)
        affected_symbols = []
        for symbol in symbols:
            if patch.affects_symbol(symbol):
                affected_symbols.append(symbol)
        return affected_symbols

    def _is_tracked_file(self, file_path: str) -> bool:
        # Implement logic to determine if a file should be tracked
        return True

    def _ensure_history_built(self) -> None:
        if not self.history_built:
            self.build_history()

    def _update_symbol_history(self, symbol: Symbol, filepath: str):
        if symbol not in self.symbol_history:
            self.symbol_history[symbol] = []
        self.symbol_history[symbol].append({
            "filepath": filepath,
            "author": self.codebase.get_author(symbol),
            "timestamp": self.codebase.get_timestamp(symbol)
        })

    def map_symbols_to_history(self, force=False) -> None:
        self._ensure_history_built()
        if force or not self.symbol_history:
            for filepath in self.codebase.get_all_filepaths():
                if self._is_tracked_file(filepath):
                    symbols = self.codebase.get_symbols(filepath)
                    for symbol in symbols:
                        self._update_symbol_history(symbol, filepath)

    def get_symbol_history(self, symbol: Symbol) -> list[dict]:
        self._ensure_history_built()
        return self.symbol_history.get(symbol, [])

    def get_symbol_last_editor(self, symbol: Symbol) -> str | None:
        history = self.get_symbol_history(symbol)
        if history:
            return history[-1]["author"]
        return None

    def get_ai_contribution_stats(self) -> dict:
        self._ensure_history_built()
        stats = {author: 0 for author in self.ai_authors}
        for symbol_history in self.symbol_history.values():
            for entry in symbol_history:
                if entry["author"] in self.ai_authors:
                    stats[entry["author"]] += 1
        return stats

    def get_ai_touched_symbols(self) -> list[Symbol]:
        self._ensure_history_built()
        ai_touched_symbols = []
        for symbol, history in self.symbol_history.items():
            for entry in history:
                if entry["author"] in self.ai_authors:
                    ai_touched_symbols.append(symbol)
                    break
        return ai_touched_symbols

    def get_ai_contribution_timeline(self) -> list[tuple[datetime, int]]:
        self._ensure_history_built()
        timeline = {}
        for symbol_history in self.symbol_history.values():
            for entry in symbol_history:
                if entry["author"] in self.ai_authors:
                    timestamp = entry["timestamp"]
                    timeline[timestamp] = timeline.get(timestamp, 0) + 1
        return sorted(timeline.items())