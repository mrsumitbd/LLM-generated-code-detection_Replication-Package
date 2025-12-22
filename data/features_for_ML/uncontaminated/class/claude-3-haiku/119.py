import requests
from typing import Optional, Dict, Any, List, Tuple

class GitHubAsset:
    def __init__(self, url: str, name: str, size: int, download_count: int, platform_info: Dict[str, str], friendly_name: str, is_updater: bool, is_utilities: bool):
        self.url = url
        self.name = name
        self.size = size
        self.download_count = download_count
        self.platform_info = platform_info
        self.friendly_name = friendly_name
        self.is_updater = is_updater
        self.is_utilities = is_utilities

class GitHubAPI:
    """GitHub API integration for IntenseRP Next updates"""

    @classmethod
    def get_latest_release(cls) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get("https://api.github.com/repos/IntenseRP/IntenseRP-Next/releases/latest")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    @classmethod
    def get_release_assets(cls, release_data: Optional[Dict[str, Any]] = None) -> List[GitHubAsset]:
        if not release_data:
            release_data = cls.get_latest_release()
        if not release_data:
            return []

        assets = []
        for asset in release_data["assets"]:
            platform_info = cls._extract_platform_info(asset["name"])
            friendly_name, is_updater, is_utilities = cls._generate_friendly_name(asset["name"], platform_info, "updater" in asset["name"], "utilities" in asset["name"])
            asset_obj = GitHubAsset(
                asset["browser_download_url"],
                asset["name"],
                asset["size"],
                asset["download_count"],
                platform_info,
                friendly_name,
                is_updater,
                is_utilities
            )
            cls._enhance_asset_metadata(asset_obj, platform_info["platform"])
            assets.append(asset_obj)
        return assets

    @classmethod
    def _enhance_asset_metadata(cls, asset: GitHubAsset, current_platform: str) -> None:
        if current_platform == "windows":
            asset.friendly_name = f"{asset.friendly_name} (Windows)"
        elif current_platform == "macos":
            asset.friendly_name = f"{asset.friendly_name} (macOS)"
        elif current_platform == "linux":
            asset.friendly_name = f"{asset.friendly_name} (Linux)"

    @classmethod
    def _extract_platform_info(cls, filename: str) -> Dict[str, str]:
        if "win" in filename:
            return {"platform": "windows", "arch": "x64" if "x64" in filename else "x86"}
        elif "mac" in filename:
            return {"platform": "macos", "arch": "x64"}
        elif "linux" in filename:
            return {"platform": "linux", "arch": "x64" if "x64" in filename else "x86"}
        else:
            return {"platform": "unknown", "arch": "unknown"}

    @classmethod
    def _generate_friendly_name(cls, filename: str, platform_info: Dict[str, str], is_updater: bool, is_utilities: bool) -> Tuple[str, bool, bool]:
        name = filename.split("-")[0]
        if is_updater:
            name = f"{name} Updater"
        elif is_utilities:
            name = f"{name} Utilities"
        if platform_info["platform"] == "windows":
            name = f"{name} ({platform_info['arch']})"
        elif platform_info["platform"] == "macos":
            name = f"{name} (macOS)"
        elif platform_info["platform"] == "linux":
            name = f"{name} ({platform_info['arch']})"
        return name, is_updater, is_utilities

    @classmethod
    def categorize_assets(cls, assets: List[GitHubAsset]) -> Dict[str, List[GitHubAsset]]:
        categories = {
            "updater": [],
            "utilities": [],
            "other": []
        }
        for asset in assets:
            if asset.is_updater:
                categories["updater"].append(asset)
            elif asset.is_utilities:
                categories["utilities"].append(asset)
            else:
                categories["other"].append(asset)
        return categories

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"