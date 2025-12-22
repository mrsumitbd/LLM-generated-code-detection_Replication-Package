from typing import Dict, Any

class ThreatMapping:
    """Mapping of threat names to MCP Taxonomy classifications with severity."""

    @classmethod
    def get_threat_mapping(cls, analyzer: str, threat_name: str) -> Dict[str, Any]:
        threat_mappings = {
            "threat1": {
                "classification": "Malware",
                "severity": "High"
            },
            "threat2": {
                "classification": "Phishing",
                "severity": "Medium"
            },
            "threat3": {
                "classification": "DDoS",
                "severity": "High"
            }
        }

        return threat_mappings.get(threat_name, {"classification": "Unknown", "severity": "Unknown"})