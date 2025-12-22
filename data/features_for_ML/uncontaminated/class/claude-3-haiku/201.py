from pathlib import Path
from typing import Optional, List, Dict, Any

class WorkspaceDetector:
    """Intelligent workspace detection for ConPort MCP server"""

    def __init__(self, start_path: Optional[str] = None, max_depth: int = 10):
        self.start_path = Path(start_path) if start_path else Path.cwd()
        self.max_depth = max_depth
        self.workspace_root = None
        self.detection_info = {}

    def find_workspace_root(self) -> Path:
        self.workspace_root = self._detect_by_strong_indicators() or self._detect_by_any_indicators() or self._detect_by_context_portal()
        return self.workspace_root

    def _detect_by_strong_indicators(self) -> Optional[Path]:
        strong_indicators = ['package.json', 'pyproject.toml']
        return self._validate_workspace(self.start_path, strong_indicators)

    def _detect_by_any_indicators(self) -> Optional[Path]:
        any_indicators = ['setup.py', 'requirements.txt', '.git', '.venv']
        return self._validate_workspace(self.start_path, any_indicators)

    def _detect_by_context_portal(self) -> Optional[Path]:
        context_portal_path = self.get_context_portal_path(self.start_path)
        if context_portal_path.exists():
            return context_portal_path.parent
        return None

    def _validate_workspace(self, path: Path, indicators: List[str]) -> Optional[Path]:
        if all(path.joinpath(indicator).exists() for indicator in indicators):
            return path
        for child in path.glob('*'):
            if child.is_dir() and child.name != '.git' and self.max_depth > 0:
                self.max_depth -= 1
                result = self._validate_workspace(child, indicators)
                if result:
                    return result
        return None

    def _validate_package_json(self, package_json_path: Path) -> bool:
        # Implement the logic to validate the package.json file
        return True

    def _validate_pyproject_toml(self, pyproject_path: Path) -> bool:
        # Implement the logic to validate the pyproject.toml file
        return True

    def get_context_portal_path(self, workspace_root: Path) -> Path:
        return workspace_root / '.conport' / 'context.json'

    def detect_from_mcp_context(self) -> Optional[str]:
        context_portal_path = self.get_context_portal_path(self.start_path)
        if context_portal_path.exists():
            # Implement the logic to read the context.json file and extract the workspace path
            return str(self.start_path)
        return None

    def get_detection_info(self) -> Dict[str, Any]:
        self.detection_info = {
            'workspace_root': str(self.workspace_root) if self.workspace_root else None,
            'detection_method': self.detection_info.get('detection_method', 'unknown')
        }
        return self.detection_info