from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import tomllib  # Python 3.11+
except Exception:
    try:
        import toml as tomllib  # type: ignore
    except Exception:
        tomllib = None  # pragma: no cover


class WorkspaceDetector:
    """Intelligent workspace detection for ConPort MCP server"""

    # Strong indicators are files that almost always mark a project root
    _STRONG_INDICATORS = [
        ".git",
        "package.json",
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
    ]

    # Any indicators are less definitive but still useful
    _ANY_INDICATORS = [
        "conport.yaml",
        "conport.json",
        "conport.toml",
    ]

    # Context portal file name
    _CONTEXT_PORTAL = ".conport/portal"

    def __init__(self, start_path: Optional[str] = None, max_depth: int = 10):
        self.start_path = Path(start_path or os.getcwd()).resolve()
        self.max_depth = max_depth
        self._workspace_root: Optional[Path] = None
        self._detected_by: Optional[str] = None
        self._indicators: List[str] = []

    def find_workspace_root(self) -> Path:
        """Return the detected workspace root or raise FileNotFoundError."""
        if self._workspace_root:
            return self._workspace_root

        # 1. Try strong indicators
        root = self._detect_by_strong_indicators()
        if root:
            self._workspace_root = root
            self._detected_by = "strong"
            return root

        # 2. Try any indicators
        root = self._detect_by_any_indicators()
        if root:
            self._workspace_root = root
            self._detected_by = "any"
            return root

        # 3. Try context portal
        root = self._detect_by_context_portal()
        if root:
            self._workspace_root = root
            self._detected_by = "context"
            return root

        raise FileNotFoundError("Could not detect a workspace root")

    def _detect_by_strong_indicators(self) -> Optional[Path]:
        """Search upwards for strong indicators."""
        return self._search_upwards(self._STRONG_INDICATORS, validate=True)

    def _detect_by_any_indicators(self) -> Optional[Path]:
        """Search upwards for any indicators."""
        return self._search_upwards(self._ANY_INDICATORS, validate=False)

    def _detect_by_context_portal(self) -> Optional[Path]:
        """Detect workspace root from MCP context portal if available."""
        context_path = self.detect_from_mcp_context()
        if context_path:
            path = Path(context_path).resolve()
            if path.is_dir():
                return path
        return None

    def _search_upwards(
        self,
        indicators: List[str],
        validate: bool = False,
    ) -> Optional[Path]:
        """Search parent directories for given indicators."""
        current = self.start_path
        depth = 0
        while depth <= self.max_depth:
            found = [p for p in indicators if (current / p).exists()]
            if found:
                if validate:
                    if self._validate_workspace(current, found):
                        self._indicators = found
                        return current
                else:
                    self._indicators = found
                    return current
            if current.parent == current:
                break
            current = current.parent
            depth += 1
        return None

    def _validate_workspace(self, path: Path, indicators: List[str]) -> bool:
        """Validate that the workspace contains required files."""
        for ind in indicators:
            if ind == "package.json":
                if not self._validate_package_json(path / ind):
                    return False
            elif ind == "pyproject.toml":
                if not self._validate_pyproject_toml(path / ind):
                    return False
        return True

    def _validate_package_json(self, package_json_path: Path) -> bool:
        """Check that package.json contains name and version."""
        try:
            with package_json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return bool(data.get("name")) and bool(data.get("version"))
        except Exception:
            return False

    def _validate_pyproject_toml(self, pyproject_path: Path) -> bool:
        """Check that pyproject.toml contains a [project] or [tool.poetry] section."""
        if not tomllib:
            return False
        try:
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
            return bool(data.get("project")) or bool(data.get("tool", {}).get("poetry"))
        except Exception:
            return False

    def get_context_portal_path(self, workspace_root: Path) -> Path:
        """Return the absolute path to the context portal file."""
        return workspace_root / self._CONTEXT_PORTAL

    def detect_from_mcp_context(self) -> Optional[str]:
        """
        Detect workspace root from MCP context.

        MCP may expose a JSON string in the environment variable
        `MCP_CONTEXT` with a key `workspace_root`. If present, return it.
        """
        ctx = os.getenv("MCP_CONTEXT")
        if not ctx:
            return None
        try:
            data = json.loads(ctx)
            return data.get("workspace_root")
        except Exception:
            return None

    def get_detection_info(self) -> Dict[str, Any]:
        """Return a dictionary with detection details."""
        try:
            root = self.find_workspace_root()
        except FileNotFoundError:
            root = None
        return {
            "workspace_root": str(root) if root else None,
            "detected_by": self._detected_by,
            "indicators": self._indicators,
            "context_portal_path": (
                str(self.get_context_portal_path(root)) if root else None
            ),
        }