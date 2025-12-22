import datetime
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import git  # pip install GitPython


class GitAttributionTracker:
    """Tracks attribution information for code symbols based on git history."""

    def __init__(self, codebase, ai_authors: Optional[List[str]] = None):
        """
        Parameters
        ----------
        codebase
            An object that provides access to the source code and its symbols.
            It must expose a ``get_symbols()`` method that returns an iterable of
            ``Symbol`` objects.
        ai_authors
            Optional list of author names that should be considered AI-generated.
        """
        self.codebase = codebase
        self.ai_authors = set(ai_authors or [])
        self.repo = git.Repo(Path(codebase.root))
        self._history: List[Dict] = []  # list of commit dicts
        self._symbol_history: Dict["Symbol", List[Dict]] = defaultdict(list)
        self._ai_touched_symbols: set["Symbol"] = set()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def build_history(self, max_commits: Optional[int] = None) -> None:
        """Build the commit history for the repository."""
        commits = list(self.repo.iter_commits(max_count=max_commits))
        for commit in commits:
            diff = commit.diff(commit.parents[0] if commit.parents else None, create_patch=True)
            self._process_commit(commit, diff)

    def map_symbols_to_history(self, force: bool = False) -> None:
        """Map each symbol to the commits that touched it."""
        if not self._history and not force:
            self._ensure_history_built()
        for commit in self._history:
            for symbol in self.codebase.get_symbols():
                if symbol in self._symbol_history:
                    continue
                if self._is_symbol_in_commit(symbol, commit):
                    self._symbol_history[symbol].append(commit)
                    if commit["author"] in self.ai_authors:
                        self._ai_touched_symbols.add(symbol)

    def get_symbol_history(self, symbol: "Symbol") -> List[Dict]:
        """Return the list of commits that touched the given symbol."""
        self._ensure_history_built()
        return self._symbol_history.get(symbol, [])

    def get_symbol_last_editor(self, symbol: "Symbol") -> Optional[str]:
        """Return the author of the most recent commit that touched the symbol."""
        history = self.get_symbol_history(symbol)
        if not history:
            return None
        return history[0]["author"]

    def get_ai_contribution_stats(self) -> Dict[str, int]:
        """Return a dictionary of AI author names to commit counts."""
        self._ensure_history_built()
        counter = Counter()
        for commit in self._history:
            if commit["author"] in self.ai_authors:
                counter[commit["author"]] += 1
        return dict(counter)

    def get_ai_touched_symbols(self) -> List["Symbol"]:
        """Return a list of symbols that were touched by AI authors."""
        self._ensure_history_built()
        return list(self._ai_touched_symbols)

    def get_ai_contribution_timeline(self) -> List[Tuple[datetime.datetime, int]]:
        """Return a timeline of AI contributions per day."""
        self._ensure_history_built()
        timeline = Counter()
        for commit in self._history:
            if commit["author"] in self.ai_authors:
                day = commit["date"].date()
                timeline[day] += 1
        return sorted([(datetime.datetime.combine(day, datetime.time.min), count)
                       for day, count in timeline.items()],
                      key=lambda x: x[0])

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _process_commit(self, commit, diff) -> None:
        """Process a single commit and store its metadata."""
        commit_dict = {
            "hash": commit.hexsha,
            "author": commit.author.name,
            "date": datetime.datetime.fromtimestamp(commit.committed_date),
            "message": commit.message.strip(),
            "diff": diff,
        }
        self._history.append(commit_dict)

    def _is_symbol_in_commit(self, symbol: "Symbol", commit: Dict) -> bool:
        """Check if the symbol was touched in the given commit."""
        for patch in commit["diff"]:
            if not self._is_tracked_file(patch.b_path):
                continue
            if self._is_symbol_in_patch(symbol, patch):
                return True
        return False

    def _is_symbol_in_patch(self, symbol: "Symbol", patch) -> bool:
        """Determine if the symbol appears in the added lines of a patch."""
        added_lines = [line[1:] for line in patch.diff.decode().splitlines()
                       if line.startswith("+") and not line.startswith("+++")]

        # Simple heuristic: if the symbol name appears in any added line
        # and the line number falls within the symbol's range, we consider it touched.
        for line in added_lines:
            if symbol.name in line:
                # Rough line number estimation: count lines up to this patch
                # This is a best‑effort approach; precise mapping would require
                # parsing the diff hunks.
                return True
        return False

    def _is_tracked_file(self, file_path: str) -> bool:
        """Return True if the file should be considered for attribution."""
        if not file_path:
            return False
        # Exclude binary files, git metadata, and hidden files
        if file_path.startswith(".git") or file_path.startswith("."):
            return False
        return True

    def _ensure_history_built(self) -> None:
        """Ensure that the commit history has been built."""
        if not self._history:
            self.build_history()
        if not self._symbol_history:
            self.map_symbols_to_history(force=True)