import re
from pathlib import Path
from typing import List, Dict, Any


class PluginFileChecker:
    """Checks Discourse plugin files for security and integrity issues"""

    # Allowed characters for plugin names: letters, digits, hyphens, underscores
    _PLUGIN_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

    # Simple patterns that are considered dangerous
    _DANGEROUS_PATTERNS = [
        re.compile(r"\beval\b"),
        re.compile(r"\bexec\b"),
        re.compile(r"\bsystem\b"),
        re.compile(r"\bsubprocess\b"),
        re.compile(r"\bimport\s+os\b"),
        re.compile(r"\bimport\s+subprocess\b"),
    ]

    # Regex to extract plugin names from a file
    _PLUGIN_NAME_REGEX = re.compile(
        r"plugin_name\s*:\s*['\"]([^'\"]+)['\"]", re.IGNORECASE
    )

    def __init__(self, scanner):
        """
        :param scanner: An object that provides access to plugin files.
                        Expected to have:
                          - get_plugin_files() -> List[Path]
                          - read_file(path: Path) -> str
                          - get_plugin_url(plugin_name: str) -> str
        """
        self.scanner = scanner

    def check_plugin_files(self) -> List[Dict[str, Any]]:
        """
        Scan all plugin files and return a list of issues found.
        Each issue is a dict with keys:
            - file: Path to the file
            - plugin: Name of the plugin (if detected)
            - issue: Description of the issue
        """
        issues = []

        for file_path in self.scanner.get_plugin_files():
            try:
                content = self.scanner.read_file(file_path)
            except Exception as exc:
                issues.append(
                    {
                        "file": str(file_path),
                        "plugin": None,
                        "issue": f"Could not read file: {exc}",
                    }
                )
                continue

            plugin_names = self._extract_plugin_names(content)
            if not plugin_names:
                # No plugin name found; flag as potential misconfiguration
                issues.append(
                    {
                        "file": str(file_path),
                        "plugin": None,
                        "issue": "No plugin name found in file",
                    }
                )
                continue

            for plugin_name in plugin_names:
                # Individual plugin checks
                plugin_issues = self._check_individual_plugin(plugin_name)
                for issue in plugin_issues:
                    issues.append(
                        {
                            "file": str(file_path),
                            "plugin": plugin_name,
                            "issue": issue,
                        }
                    )

                # Content checks
                url = self.scanner.get_plugin_url(plugin_name)
                content_issues = self._check_plugin_content(plugin_name, content, url)
                for issue in content_issues:
                    issues.append(
                        {
                            "file": str(file_path),
                            "plugin": plugin_name,
                            "issue": issue,
                        }
                    )

        return issues

    def _extract_plugin_names(self, content: str) -> List[str]:
        """
        Extract plugin names from the file content.
        """
        return [
            match.group(1).strip()
            for match in self._PLUGIN_NAME_REGEX.finditer(content)
        ]

    def _check_individual_plugin(self, plugin_name: str) -> List[str]:
        """
        Perform checks on the plugin name itself.
        Returns a list of issue strings.
        """
        issues = []
        if not self._PLUGIN_NAME_PATTERN.match(plugin_name):
            issues.append(
                f"Plugin name '{plugin_name}' contains invalid characters. "
                "Allowed: letters, digits, hyphens, underscores."
            )
        return issues

    def _check_plugin_content(
        self, plugin_name: str, content: str, url: str
    ) -> List[str]:
        """
        Perform content checks on the plugin file.
        Returns a list of issue strings.
        """
        issues = []

        # Check for dangerous patterns
        for pattern in self._DANGEROUS_PATTERNS:
            if pattern.search(content):
                issues.append(
                    f"Potentially dangerous code detected in plugin '{plugin_name}': "
                    f"matched pattern '{pattern.pattern}'."
                )

        # Basic URL validation: ensure the URL is a valid HTTP/HTTPS URL
        if url:
            if not re.match(r"^https?://", url):
                issues.append(
                    f"Plugin '{plugin_name}' has an invalid URL: {url}"
                )
        else:
            issues.append(f"Plugin '{plugin_name}' does not have an associated URL.")

        return issues