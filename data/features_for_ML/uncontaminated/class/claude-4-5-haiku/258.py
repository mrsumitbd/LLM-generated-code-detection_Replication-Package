class GitAttributionTracker:
    """Tracks attribution information for code symbols based on git history."""

    def __init__(self, codebase: Codebase, ai_authors: list[str] | None = None):
        self.codebase = codebase
        self.ai_authors = ai_authors or []
        self.repo = codebase.repo
        self.symbol_history = {}
        self.history_built = False
        self.commit_history = []
        self.ai_contribution_stats = {
            'total_commits': 0,
            'total_symbols_touched': 0,
            'symbols_by_ai': set(),
            'commits_by_ai': []
        }

    def build_history(self, max_commits: int | None = None) -> None:
        """Build git history for the codebase."""
        self.commit_history = []
        commits = list(self.repo.iter_commits())
        
        if max_commits:
            commits = commits[:max_commits]
        
        for i, commit in enumerate(commits):
            if i > 0:
                prev_commit = commits[i - 1]
                diff = self.repo.git.diff(prev_commit.hexsha, commit.hexsha, 
                                         unified=0, no_prefix=True)
            else:
                diff = self.repo.git.show(commit.hexsha, unified=0, no_prefix=True)
            
            self._process_commit(commit, diff)
        
        self.history_built = True

    def _process_commit(self, commit, diff) -> None:
        """Process a single commit and extract attribution information."""
        commit_info = {
            'hexsha': commit.hexsha,
            'author': commit.author.name,
            'email': commit.author.email,
            'timestamp': commit.committed_datetime,
            'message': commit.message,
            'is_ai': commit.author.name in self.ai_authors or 
                    commit.author.email in self.ai_authors
        }
        
        self.commit_history.append(commit_info)
        
        if commit_info['is_ai']:
            self.ai_contribution_stats['total_commits'] += 1
            self.ai_contribution_stats['commits_by_ai'].append(commit_info)
        
        affected_files = set()
        for item in commit.tree.traverse():
            if item.type == 'blob':
                affected_files.add(item.path)
        
        self._process_symbol_location_state(list(affected_files))

    def _process_symbol_location_state(self, filepaths: list[str]):
        """Process symbol locations affected by file changes."""
        for filepath in filepaths:
            if self._is_tracked_file(filepath):
                try:
                    symbols = self.codebase.get_symbols_in_file(filepath)
                    for symbol in symbols:
                        if symbol not in self.symbol_history:
                            self.symbol_history[symbol] = []
                except Exception:
                    pass

    def _get_symbols_affected_by_patch(self, patch: Patch, filepath):
        """Extract symbols affected by a patch."""
        affected_symbols = []
        try:
            symbols = self.codebase.get_symbols_in_file(filepath)
            for symbol in symbols:
                if hasattr(symbol, 'lineno'):
                    for hunk in patch:
                        if hunk.source_start <= symbol.lineno <= hunk.source_start + hunk.source_length:
                            affected_symbols.append(symbol)
                            break
        except Exception:
            pass
        return affected_symbols

    def _is_tracked_file(self, file_path: str) -> bool:
        """Check if a file should be tracked."""
        if not file_path:
            return False
        
        excluded_extensions = {'.pyc', '.pyo', '.so', '.o', '.a'}
        if any(file_path.endswith(ext) for ext in excluded_extensions):
            return False
        
        tracked_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs'}
        return any(file_path.endswith(ext) for ext in tracked_extensions)

    def _ensure_history_built(self) -> None:
        """Ensure git history has been built."""
        if not self.history_built:
            self.build_history()

    def map_symbols_to_history(self, force=False) -> None:
        """Map symbols to their git history."""
        self._ensure_history_built()
        
        if self.symbol_history and not force:
            return
        
        self.symbol_history = {}
        
        for commit_info in self.commit_history:
            commit = self.repo.commit(commit_info['hexsha'])
            
            for item in commit.tree.traverse():
                if item.type == 'blob' and self._is_tracked_file(item.path):
                    try:
                        symbols = self.codebase.get_symbols_in_file(item.path)
                        for symbol in symbols:
                            if symbol not in self.symbol_history:
                                self.symbol_history[symbol] = []
                            
                            self.symbol_history[symbol].append(commit_info)
                            
                            if commit_info['is_ai']:
                                self.ai_contribution_stats['symbols_by_ai'].add(symbol)
                    except Exception:
                        pass

    def get_symbol_history(self, symbol: Symbol) -> list[dict]:
        """Get the git history for a specific symbol."""
        self._ensure_history_built()
        return self.symbol_history.get(symbol, [])

    def get_symbol_last_editor(self, symbol: Symbol) -> str | None:
        """Get the last editor of a symbol."""
        history = self.get_symbol_history(symbol)
        if history:
            return history[-1]['author']
        return None

    def get_ai_contribution_stats(self) -> dict:
        """Get statistics about AI contributions."""
        self._ensure_history_built()
        return {
            'total_commits': self.ai_contribution_stats['total_commits'],
            'total_symbols_touched': len(self.ai_contribution_stats['symbols_by_ai']),
            'symbols_touched': list(self.ai_contribution_stats['symbols_by_ai'])
        }

    def get_ai_touched_symbols(self) -> list[Symbol]:
        """Get all symbols touched by AI authors."""
        self._ensure_history_built()
        return list(self.ai_contribution_stats['symbols_by_ai'])

    def get_ai_contribution_timeline(self) -> list[tuple[datetime, int]]:
        """Get a timeline of AI contributions."""
        self._ensure_history_built()
        timeline = {}
        
        for commit_info in self.ai_contribution_stats['commits_by_ai']:
            date = commit_info['timestamp'].date()
            timeline[date] = timeline.get(date, 0) + 1
        
        return sorted([(date, count) for date, count in timeline.items()])