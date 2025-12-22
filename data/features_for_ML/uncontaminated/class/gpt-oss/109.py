import re
import urllib.parse
from collections import defaultdict

class AssetFileChecker:
    """Checks asset files for security vulnerabilities and malicious content"""

    def __init__(self, scanner):
        """
        :param scanner: An object that provides the following methods:
            - get_assets() -> list of asset URLs
            - fetch(url) -> content of the asset
            - scan(content) -> list of issue dicts found in the content
        """
        self.scanner = scanner
        self.asset_files = []          # List of dicts: {'url': str, 'content': str, 'issues': list}
        self.summary = {}              # Final summary dictionary

    def run(self):
        """Run the full asset checking pipeline."""
        self.check_asset_files()
        self.analyze_javascript_endpoints()
        self.analyze_discourse_robots_sitemap()
        self._generate_summary()
        return self.summary

    def check_asset_files(self):
        """Retrieve and scan all asset files."""
        for asset_url in self.scanner.get_assets():
            try:
                content = self.scanner.fetch(asset_url)
            except Exception:
                continue  # Skip assets that cannot be fetched
            issues = self._check_asset_content(asset_url, content, asset_url)
            self.asset_files.append({
                'url': asset_url,
                'content': content,
                'issues': issues
            })

    def _extract_asset_files(self, content, base_path):
        """
        Extract asset URLs from HTML-like content.
        :param content: The raw content string.
        :param base_path: Base URL to resolve relative paths.
        :return: List of absolute URLs.
        """
        pattern = r'(?:src|href)\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content, re.IGNORECASE)
        resolved = [urllib.parse.urljoin(base_path, m) for m in matches]
        return resolved

    def _check_asset_content(self, asset_file, content, url):
        """
        Scan the content of an asset for issues.
        :param asset_file: The asset URL (unused but kept for signature).
        :param content: Raw content string.
        :param url: The URL of the asset.
        :return: List of issue dictionaries.
        """
        issues = self.scanner.scan(content)
        for issue in issues:
            issue.setdefault('url', url)
        return issues

    def _check_asset_file(self, asset_file):
        """
        Placeholder for file-level checks (e.g., size, permissions).
        Currently returns an empty list.
        """
        return []

    def get_asset_security_summary(self, all_issues):
        """
        Aggregate issues by type.
        :param all_issues: List of issue dictionaries.
        :return: Dict mapping issue type to count.
        """
        summary = defaultdict(int)
        for issue in all_issues:
            issue_type = issue.get('type', 'unknown')
            summary[issue_type] += 1
        return dict(summary)

    def analyze_javascript_endpoints(self):
        """
        Find URLs referenced inside JavaScript assets.
        Stores the list in self.summary['javascript_endpoints'].
        """
        endpoints = []
        for asset in self.asset_files:
            if asset['url'].lower().endswith('.js'):
                pattern = r'["\'](https?://[^"\']+)["\']'
                endpoints.extend(re.findall(pattern, asset['content']))
        self.summary['javascript_endpoints'] = endpoints

    def analyze_discourse_robots_sitemap(self):
        """
        Extract the contents of robots.txt and sitemap.xml if present.
        Stores them in self.summary['robots'] and self.summary['sitemap'].
        """
        robots = None
        sitemap = None
        for asset in self.asset_files:
            if asset['url'].lower().endswith('robots.txt'):
                robots = asset['content']
            if asset['url'].lower().endswith('sitemap.xml'):
                sitemap = asset['content']
        self.summary['robots'] = robots
        self.summary['sitemap'] = sitemap

    def _generate_summary(self):
        """Compile the final summary dictionary."""
        all_issues = []
        for asset in self.asset_files:
            all_issues.extend(asset['issues'])
        self.summary['issues'] = all_issues
        self.summary['issue_summary'] = self.get_asset_security_summary(all_issues)