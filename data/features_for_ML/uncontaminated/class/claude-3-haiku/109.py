import os
import re
from typing import List, Tuple
from .scanner import Scanner

class AssetFileChecker:
    """Checks asset files for security vulnerabilities and malicious content"""

    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.asset_files = []
        self.asset_security_issues = []

    def run(self):
        self.check_asset_files()
        self.analyze_javascript_endpoints()
        self.analyze_discourse_robots_sitemap()
        return self.get_asset_security_summary(self.asset_security_issues)

    def check_asset_files(self):
        for root, dirs, files in os.walk("assets"):
            for file in files:
                asset_file = os.path.join(root, file)
                content = open(asset_file, "r").read()
                url = f"/{asset_file.replace('assets/', '')}"
                issues = self._check_asset_file(asset_file)
                if issues:
                    self.asset_security_issues.extend(issues)

    def _extract_asset_files(self, content: str, base_path: str) -> List[Tuple[str, str]]:
        asset_files = []
        pattern = r'src="([^"]+)"'
        for match in re.finditer(pattern, content):
            asset_url = match.group(1)
            asset_path = os.path.join(base_path, asset_url.lstrip("/"))
            asset_files.append((asset_path, asset_url))
        return asset_files

    def _check_asset_content(self, asset_file: str, content: str, url: str) -> List[dict]:
        issues = self.scanner.scan_content(content, url)
        return issues

    def _check_asset_file(self, asset_file: str) -> List[dict]:
        content = open(asset_file, "r").read()
        url = f"/{asset_file.replace('assets/', '')}"
        issues = self._check_asset_content(asset_file, content, url)
        return issues

    def get_asset_security_summary(self, all_issues: List[dict]) -> dict:
        summary = self._generate_summary()
        return summary

    def analyze_javascript_endpoints(self):
        pass

    def analyze_discourse_robots_sitemap(self):
        pass

    def _generate_summary(self) -> dict:
        summary = {
            "total_issues": len(self.asset_security_issues),
            "issues_by_type": {},
            "issues_by_severity": {},
        }
        for issue in self.asset_security_issues:
            issue_type = issue["type"]
            issue_severity = issue["severity"]
            summary["issues_by_type"].setdefault(issue_type, 0)
            summary["issues_by_type"][issue_type] += 1
            summary["issues_by_severity"].setdefault(issue_severity, 0)
            summary["issues_by_severity"][issue_severity] += 1
        return summary