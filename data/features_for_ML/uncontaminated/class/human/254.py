from src.string_utils import safe_format

class FallbackRepoManager:
            @staticmethod
            def read_xdc_constraints(board: str) -> str:
                return safe_format(
                    "# Fallback XDC constraints for board: {board}\n"
                    "# RepoManager not available",
                    board=board,
                )

            @staticmethod
            def read_combined_xdc(board: str) -> str:
                return safe_format(
                    "# Fallback XDC constraints for board: {board}\n"
                    "# RepoManager not available",
                    board=board,
                )

            @staticmethod
            def ensure_git_repo():
                raise RuntimeError(
                    "RepoManager not available - git operations disabled"
                )