import os
import requests
from bs4 import BeautifulSoup

class PluginFileChecker:
    """Checks Discourse plugin files for security and integrity issues"""

    def __init__(self, scanner):
        self.scanner = scanner

    def check_plugin_files(self):
        plugin_names = self._extract_plugin_names(os.listdir('plugins'))
        for plugin_name in plugin_names:
            self._check_individual_plugin(plugin_name)

    def _extract_plugin_names(self, content):
        plugin_names = []
        for item in content:
            if os.path.isdir(os.path.join('plugins', item)):
                plugin_names.append(item)
        return plugin_names

    def _check_individual_plugin(self, plugin_name):
        plugin_path = os.path.join('plugins', plugin_name)
        for root, dirs, files in os.walk(plugin_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                self._check_plugin_content(plugin_name, content, file_path)

    def _check_plugin_content(self, plugin_name, content, url):
        issues = self.scanner.scan_content(content)
        if issues:
            print(f"Issues found in plugin '{plugin_name}' at {url}:")
            for issue in issues:
                print(f"- {issue}")