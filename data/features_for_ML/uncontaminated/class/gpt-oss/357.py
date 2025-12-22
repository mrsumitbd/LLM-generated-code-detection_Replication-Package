from typing import Any, Dict

class ThreatMapping:
    """Mapping of threat names to MCP Taxonomy classifications with severity."""

    # Static mapping of analyzers → threat names → taxonomy & severity
    _MAPPING: Dict[str, Dict[str, Dict[str, Any]]] = {
        "analyzer_a": {
            "SQL Injection": {
                "taxonomy": "Injection",
                "severity": "High",
            },
            "Cross-Site Scripting": {
                "taxonomy": "XSS",
                "severity": "Medium",
            },
            "Privilege Escalation": {
                "taxonomy": "Privilege Escalation",
                "severity": "Critical",
            },
        },
        "analyzer_b": {
            "Phishing": {
                "taxonomy": "Social Engineering",
                "severity": "High",
            },
            "Malware": {
                "taxonomy": "Malware",
                "severity": "Critical",
            },
            "Denial of Service": {
                "taxonomy": "DoS",
                "severity": "Medium",
            },
        },
        # Default analyzer mapping (fallback)
        "default": {
            "Unknown Threat": {
                "taxonomy": "Unknown",
                "severity": "Low",
            },
        },
    }

    @classmethod
    def get_threat_mapping(cls, analyzer: str, threat_name: str) -> Dict[str, Any]:
        """
        Return the taxonomy classification and severity for a given threat name
        under the specified analyzer.

        Parameters
        ----------
        analyzer : str
            Identifier of the analyzer (e.g., 'analyzer_a', 'analyzer_b').
        threat_name : str
            Human‑readable name of the threat.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing 'taxonomy' and 'severity' keys. If the
            threat is not found, returns an empty dictionary.
        """
        # Use the specified analyzer mapping if available, otherwise fall back to default
        analyzer_map = cls._MAPPING.get(analyzer, cls._MAPPING.get("default", {}))
        return analyzer_map.get(threat_name, {})