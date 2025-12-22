from typing import Dict, Any

class ThreatMapping:
    """Mapping of threat names to MCP Taxonomy classifications with severity."""

    _THREAT_MAPPING = {
        "Malware": {
            "taxonomy": "Malicious Code",
            "severity": "High"
        },
        "Phishing": {
            "taxonomy": "Social Engineering",
            "severity": "High"
        },
        "Ransomware": {
            "taxonomy": "Malicious Code",
            "severity": "Critical"
        },
        "SQL Injection": {
            "taxonomy": "Injection",
            "severity": "High"
        },
        "Cross-Site Scripting (XSS)": {
            "taxonomy": "Injection",
            "severity": "High"
        }
    }

    @classmethod
    def get_threat_mapping(cls, analyzer: str, threat_name: str) -> Dict[str, Any]:
        """
        Retrieve the MCP Taxonomy classification and severity for a given threat name.

        Args:
            analyzer (str): The name of the analyzer that detected the threat.
            threat_name (str): The name of the threat.

        Returns:
            Dict[str, Any]: A dictionary containing the MCP Taxonomy classification and severity for the given threat name.
        """
        if threat_name in cls._THREAT_MAPPING:
            return cls._THREAT_MAPPING[threat_name]
        else:
            return {
                "taxonomy": "Unknown",
                "severity": "Unknown"
            }