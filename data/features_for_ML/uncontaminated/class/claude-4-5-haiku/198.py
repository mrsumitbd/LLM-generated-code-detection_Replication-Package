import anthropic
import json
from typing import Any, Dict


class PluginBruteforceModule:
    """Plugin discovery via bruteforce (Refactored)"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.discovered_plugins = []
        self.plugin_patterns = [
            "/wp-content/plugins/",
            "/plugins/",
            "/modules/",
            "/extensions/",
            "/addons/",
        ]

    def run(self) -> Dict[str, Any]:
        """Execute the plugin bruteforce module"""
        self.discovered_plugins = []
        self._bruteforce_plugins()

        return {
            "module": "plugin_bruteforce",
            "discovered_plugins": self.discovered_plugins,
            "total_found": len(self.discovered_plugins),
        }

    def _bruteforce_plugins(self):
        """Bruteforce plugin discovery using Claude AI"""
        target_url = self.scanner.get("target_url", "http://example.com")

        prompt = f"""You are a security researcher analyzing potential plugins for a web application at {target_url}.

Based on common plugin naming conventions and patterns, generate a list of 20 likely plugin names that might be installed on this WordPress/CMS site. Consider:
1. Popular WordPress plugins
2. Common naming patterns
3. Security-related plugins
4. Performance optimization plugins
5. SEO plugins

For each plugin, provide:
- Plugin name
- Common directory path
- Likelihood score (1-10)
- Potential security implications

Format your response as a JSON array with objects containing: name, path, likelihood, security_notes"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        try:
            json_start = response_text.find("[")
            json_end = response_text.rfind("]") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                plugins = json.loads(json_str)

                for plugin in plugins:
                    if isinstance(plugin, dict):
                        self.discovered_plugins.append(
                            {
                                "name": plugin.get("name", "Unknown"),
                                "path": plugin.get("path", ""),
                                "likelihood": plugin.get("likelihood", 5),
                                "security_notes": plugin.get("security_notes", ""),
                                "status": "potential",
                            }
                        )
        except (json.JSONDecodeError, ValueError):
            lines = response_text.split("\n")
            for line in lines:
                if line.strip() and not line.startswith("#"):
                    self.discovered_plugins.append(
                        {
                            "name": line.strip(),
                            "path": f"/wp-content/plugins/{line.strip()}/",
                            "likelihood": 5,
                            "security_notes": "Extracted from AI response",
                            "status": "potential",
                        }
                    )