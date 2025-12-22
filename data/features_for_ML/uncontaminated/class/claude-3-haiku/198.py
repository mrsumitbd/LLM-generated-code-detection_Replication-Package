import os
import importlib
from typing import Dict, Any

class PluginBruteforceModule:
    """Plugin discovery via bruteforce (Refactored)"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.plugin_directory = os.path.join(os.path.dirname(__file__), 'plugins')

    def run(self) -> Dict[str, Any]:
        return self._bruteforce_plugins()

    def _bruteforce_plugins(self):
        discovered_plugins = {}
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = os.path.splitext(filename)[0]
                try:
                    module = importlib.import_module(f'plugins.{module_name}')
                    plugin_class = getattr(module, 'Plugin')
                    plugin_instance = plugin_class(self.scanner)
                    plugin_name = plugin_instance.get_name()
                    discovered_plugins[plugin_name] = plugin_instance
                except (ImportError, AttributeError):
                    continue
        return discovered_plugins