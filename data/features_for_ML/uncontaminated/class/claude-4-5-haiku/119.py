class GitHubAPI:
    """GitHub API integration for IntenseRP Next updates"""

    GITHUB_REPO = "IntenseRP/IntenseRP-Next"
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"
    TIMEOUT = 10

    @classmethod
    def get_latest_release(cls) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(
                f"{cls.GITHUB_API_URL}/releases/latest",
                timeout=cls.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError):
            return None

    @classmethod
    def get_release_assets(cls, release_data: Optional[Dict[str, Any]] = None) -> List[GitHubAsset]:
        if release_data is None:
            release_data = cls.get_latest_release()
        
        if not release_data or "assets" not in release_data:
            return []
        
        assets = []
        current_platform = platform.system()
        
        for asset_data in release_data["assets"]:
            asset = GitHubAsset(
                name=asset_data.get("name", ""),
                url=asset_data.get("browser_download_url", ""),
                size=asset_data.get("size", 0),
                download_count=asset_data.get("download_count", 0),
                created_at=asset_data.get("created_at", ""),
                updated_at=asset_data.get("updated_at", "")
            )
            cls._enhance_asset_metadata(asset, current_platform)
            assets.append(asset)
        
        return assets

    @classmethod
    def _enhance_asset_metadata(cls, asset: GitHubAsset, current_platform: str) -> None:
        platform_info = cls._extract_platform_info(asset.name)
        is_updater = "updater" in asset.name.lower()
        is_utilities = "utilities" in asset.name.lower() or "utils" in asset.name.lower()
        
        friendly_name, category = cls._generate_friendly_name(
            asset.name, platform_info, is_updater, is_utilities
        )
        
        asset.friendly_name = friendly_name
        asset.category = category
        asset.platform = platform_info.get("platform", "Unknown")
        asset.architecture = platform_info.get("architecture", "Unknown")
        asset.is_compatible = cls._is_compatible(platform_info, current_platform)
        asset.formatted_size = cls.format_file_size(asset.size)

    @classmethod
    def _extract_platform_info(cls, filename: str) -> Dict[str, str]:
        filename_lower = filename.lower()
        
        platform_map = {
            "windows": "Windows",
            "win": "Windows",
            "linux": "Linux",
            "macos": "macOS",
            "mac": "macOS",
            "darwin": "macOS"
        }
        
        arch_map = {
            "x64": "x64",
            "x86_64": "x64",
            "amd64": "x64",
            "x86": "x86",
            "i386": "x86",
            "arm64": "ARM64",
            "aarch64": "ARM64"
        }
        
        platform_detected = "Unknown"
        architecture_detected = "Unknown"
        
        for key, value in platform_map.items():
            if key in filename_lower:
                platform_detected = value
                break
        
        for key, value in arch_map.items():
            if key in filename_lower:
                architecture_detected = value
                break
        
        return {
            "platform": platform_detected,
            "architecture": architecture_detected
        }

    @classmethod
    def _generate_friendly_name(cls, filename: str, platform_info: Dict[str, str], is_updater: bool, is_utilities: bool) -> Tuple[str, str]:
        name_without_ext = filename.rsplit(".", 1)[0]
        
        if is_updater:
            category = "Updater"
            friendly = f"IntenseRP Updater ({platform_info.get('platform', 'Unknown')} {platform_info.get('architecture', 'Unknown')})"
        elif is_utilities:
            category = "Utilities"
            friendly = f"IntenseRP Utilities ({platform_info.get('platform', 'Unknown')} {platform_info.get('architecture', 'Unknown')})"
        else:
            category = "Main"
            friendly = f"IntenseRP Next ({platform_info.get('platform', 'Unknown')} {platform_info.get('architecture', 'Unknown')})"
        
        return friendly, category

    @classmethod
    def categorize_assets(cls, assets: List[GitHubAsset]) -> Dict[str, List[GitHubAsset]]:
        categorized = {
            "Main": [],
            "Updater": [],
            "Utilities": [],
            "Other": []
        }
        
        for asset in assets:
            category = asset.category if hasattr(asset, 'category') else "Other"
            if category in categorized:
                categorized[category].append(asset)
            else:
                categorized["Other"].append(asset)
        
        return categorized

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"

    @classmethod
    def _is_compatible(cls, platform_info: Dict[str, str], current_platform: str) -> bool:
        platform_map = {
            "Windows": "Windows",
            "Linux": "Linux",
            "Darwin": "macOS"
        }
        
        detected_platform = platform_info.get("platform", "Unknown")
        current_mapped = platform_map.get(current_platform, current_platform)
        
        return detected_platform == current_mapped