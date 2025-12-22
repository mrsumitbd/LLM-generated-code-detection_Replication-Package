from typing import Optional, Dict, Any, List, Tuple

class GitHubAPI:
    """GitHub API integration for IntenseRP Next updates"""

    @classmethod
    def get_latest_release(cls) -> Optional[Dict[str, Any]]:
        pass

    @classmethod
    def get_release_assets(cls, release_data: Optional[Dict[str, Any]] = None) -> List[GitHubAsset]:
        pass

    @classmethod
    def _enhance_asset_metadata(cls, asset: GitHubAsset, current_platform: str) -> None:
        pass

    @classmethod
    def _extract_platform_info(cls, filename: str) -> Dict[str, str]:
        pass

    @classmethod
    def _generate_friendly_name(cls, filename: str, platform_info: Dict[str, str], is_updater: bool, is_utilities: bool) -> Tuple[str, str]:
        pass

    @classmethod
    def categorize_assets(cls, assets: List[GitHubAsset]) -> Dict[str, List[GitHubAsset]]:
        pass

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        pass