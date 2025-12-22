import os
import re
import requests
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class GitHubAsset:
    name: str
    url: str
    size: int
    platform: str = field(default="")
    friendly_name: str = field(default="")
    is_updater: bool = field(default=False)
    is_utilities: bool = field(default=False)

class GitHubAPI:
    """GitHub API integration for IntenseRP Next updates"""

    _BASE_URL = "https://api.github.com"
    _REPO = "IntenseRP/Next"

    @classmethod
    def _request(cls, endpoint: str) -> Optional[Dict[str, Any]]:
        headers = {}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        try:
            resp = requests.get(f"{cls._BASE_URL}{endpoint}", headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    @classmethod
    def get_latest_release(cls) -> Optional[Dict[str, Any]]:
        return cls._request(f"/repos/{cls._REPO}/releases/latest")

    @classmethod
    def get_release_assets(
        cls, release_data: Optional[Dict[str, Any]] = None
    ) -> List[GitHubAsset]:
        if release_data is None:
            release_data = cls.get_latest_release()
            if release_data is None:
                return []

        assets = []
        for asset in release_data.get("assets", []):
            ga = GitHubAsset(
                name=asset.get("name", ""),
                url=asset.get("browser_download_url", ""),
                size=asset.get("size", 0),
            )
            cls._enhance_asset_metadata(ga, os.name)
            assets.append(ga)
        return assets

    @classmethod
    def _enhance_asset_metadata(cls, asset: GitHubAsset, current_platform: str) -> None:
        platform_info = cls._extract_platform_info(asset.name)
        asset.platform = platform_info.get("platform", "")
        asset.is_updater = "updater" in asset.name.lower()
        asset.is_utilities = "utilities" in asset.name.lower()
        friendly_name, _ = cls._generate_friendly_name(
            asset.name, platform_info, asset.is_updater, asset.is_utilities
        )
        asset.friendly_name = friendly_name

    @classmethod
    def _extract_platform_info(cls, filename: str) -> Dict[str, str]:
        info: Dict[str, str] = {}
        lower = filename.lower()
        if "windows" in lower or "win" in lower:
            info["platform"] = "Windows"
        elif "linux" in lower:
            info["platform"] = "Linux"
        elif "mac" in lower or "darwin" in lower:
            info["platform"] = "macOS"
        else:
            info["platform"] = "Unknown"

        arch = None
        if re.search(r"x86_64|amd64", lower):
            arch = "x86_64"
        elif re.search(r"arm64|aarch64", lower):
            arch = "ARM64"
        if arch:
            info["arch"] = arch
        return info

    @classmethod
    def _generate_friendly_name(
        cls,
        filename: str,
        platform_info: Dict[str, str],
        is_updater: bool,
        is_utilities: bool,
    ) -> Tuple[str, str]:
        base = os.path.splitext(filename)[0]
        parts = [base]
        if platform_info.get("platform"):
            parts.append(platform_info["platform"])
        if platform_info.get("arch"):
            parts.append(platform_info["arch"])
        if is_updater:
            parts.append("Updater")
        if is_utilities:
            parts.append("Utilities")
        friendly = " ".join(parts)
        return friendly, base

    @classmethod
    def categorize_assets(cls, assets: List[GitHubAsset]) -> Dict[str, List[GitHubAsset]]:
        categories: Dict[str, List[GitHubAsset]] = {"updater": [], "utilities": [], "main": []}
        for asset in assets:
            if asset.is_updater:
                categories["updater"].append(asset)
            elif asset.is_utilities:
                categories["utilities"].append(asset)
            else:
                categories["main"].append(asset)
        return categories

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        for unit in ("KB", "MB", "GB", "TB"):
            size_bytes /= 1024.0
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
        return f"{size_bytes:.2f} PB"