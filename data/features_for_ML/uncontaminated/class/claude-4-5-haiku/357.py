import anthropic
from typing import Any


class ThreatMapping:
    """Mapping of threat names to MCP Taxonomy classifications with severity."""

    @classmethod
    def get_threat_mapping(cls, analyzer: str, threat_name: str) -> dict[str, Any]:
        """
        Get MCP Taxonomy classification for a threat using Claude.
        
        Args:
            analyzer: The name of the security analyzer/tool
            threat_name: The name of the threat to classify
            
        Returns:
            A dictionary containing the threat mapping with MCP Taxonomy classification
        """
        client = anthropic.Anthropic()
        
        prompt = f"""You are a cybersecurity expert. Map the following threat to the MCP (MITRE ATT&CK) Taxonomy.

Analyzer: {analyzer}
Threat Name: {threat_name}

Provide the mapping in the following JSON format:
{{
    "threat_name": "{threat_name}",
    "analyzer": "{analyzer}",
    "mitre_attack_techniques": ["T1234", "T5678"],
    "mitre_attack_tactics": ["Reconnaissance", "Initial Access"],
    "severity": "high",
    "description": "Brief description of the threat",
    "recommendations": ["Recommendation 1", "Recommendation 2"]
}}

Return only valid JSON, no additional text."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        import json
        threat_mapping = json.loads(response_text)
        
        return threat_mapping