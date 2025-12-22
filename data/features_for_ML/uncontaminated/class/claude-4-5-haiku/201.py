class WorkspaceDetector:
    """Intelligent workspace detection for ConPort MCP server"""

    def __init__(self, start_path: Optional[str] = None, max_depth: int = 10):
        self.start_path = Path(start_path) if start_path else Path.cwd()
        self.max_depth = max_depth
        self.detection_info = {}
        
        # Strong indicators (must be valid)
        self.strong_indicators = [
            "package.json",
            "pyproject.toml",
            ".git",
            "workspace.json",
            "conport.config.json"
        ]
        
        # Any indicators (at least one should exist)
        self.any_indicators = [
            "package.json",
            "pyproject.toml",
            ".git",
            "README.md",
            "src",
            "lib",
            "workspace.json",
            "conport.config.json"
        ]

    def find_workspace_root(self) -> Path:
        """Find the workspace root by checking for indicators"""
        # Try strong indicators first
        result = self._detect_by_strong_indicators()
        if result:
            self.detection_info["method"] = "strong_indicators"
            return result
        
        # Try any indicators
        result = self._detect_by_any_indicators()
        if result:
            self.detection_info["method"] = "any_indicators"
            return result
        
        # Try context portal
        result = self._detect_by_context_portal()
        if result:
            self.detection_info["method"] = "context_portal"
            return result
        
        # Fall back to start path
        self.detection_info["method"] = "fallback"
        return self.start_path

    def _detect_by_strong_indicators(self) -> Optional[Path]:
        """Detect workspace by strong indicators that must be valid"""
        current = self.start_path
        
        for _ in range(self.max_depth):
            if self._validate_workspace(current, self.strong_indicators):
                return current
            
            parent = current.parent
            if parent == current:
                break
            current = parent
        
        return None

    def _detect_by_any_indicators(self) -> Optional[Path]:
        """Detect workspace by presence of any indicators"""
        current = self.start_path
        
        for _ in range(self.max_depth):
            found_indicators = []
            for indicator in self.any_indicators:
                if (current / indicator).exists():
                    found_indicators.append(indicator)
            
            if found_indicators:
                return current
            
            parent = current.parent
            if parent == current:
                break
            current = parent
        
        return None

    def _detect_by_context_portal(self) -> Optional[Path]:
        """Detect workspace by context portal file"""
        current = self.start_path
        
        for _ in range(self.max_depth):
            context_portal = current / ".context-portal"
            if context_portal.exists():
                try:
                    content = context_portal.read_text().strip()
                    if content:
                        return Path(content)
                except Exception:
                    pass
            
            parent = current.parent
            if parent == current:
                break
            current = parent
        
        return None

    def _validate_workspace(self, path: Path, indicators: List[str]) -> bool:
        """Validate workspace by checking indicators"""
        for indicator in indicators:
            indicator_path = path / indicator
            
            if indicator == "package.json":
                if indicator_path.exists() and self._validate_package_json(indicator_path):
                    return True
            elif indicator == "pyproject.toml":
                if indicator_path.exists() and self._validate_pyproject_toml(indicator_path):
                    return True
            elif indicator in [".git", "workspace.json", "conport.config.json"]:
                if indicator_path.exists():
                    return True
        
        return False

    def _validate_package_json(self, package_json_path: Path) -> bool:
        """Validate package.json file"""
        try:
            import json
            content = json.loads(package_json_path.read_text())
            return isinstance(content, dict) and ("name" in content or "version" in content)
        except Exception:
            return False

    def _validate_pyproject_toml(self, pyproject_path: Path) -> bool:
        """Validate pyproject.toml file"""
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                return pyproject_path.exists()
        
        try:
            with open(pyproject_path, "rb") as f:
                content = tomllib.load(f)
            return isinstance(content, dict) and (
                "project" in content or "tool" in content or "build-system" in content
            )
        except Exception:
            return False

    def get_context_portal_path(self, workspace_root: Path) -> Path:
        """Get the context portal file path for a workspace"""
        return workspace_root / ".context-portal"

    def detect_from_mcp_context(self) -> Optional[str]:
        """Detect workspace from MCP context environment"""
        import os
        
        mcp_context = os.environ.get("MCP_CONTEXT")
        if mcp_context:
            try:
                return str(Path(mcp_context).resolve())
            except Exception:
                pass
        
        return None

    def get_detection_info(self) -> Dict[str, Any]:
        """Get information about the detection process"""
        return {
            "start_path": str(self.start_path),
            "max_depth": self.max_depth,
            "method": self.detection_info.get("method", "unknown"),
            "strong_indicators": self.strong_indicators,
            "any_indicators": self.any_indicators
        }