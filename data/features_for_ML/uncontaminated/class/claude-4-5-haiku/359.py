import anthropic
import json
from typing import Any, Optional, Dict


class AdminPanelModule:
    """Admin panel security testing"""

    def __init__(self, target_url: str, session: Optional[Any] = None, verbose: bool = False):
        self.target_url = target_url
        self.session = session
        self.verbose = verbose
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def scan(self) -> Dict[str, Any]:
        """Scan admin panel for security vulnerabilities using Claude"""
        
        prompt = f"""You are a security expert performing a comprehensive admin panel security assessment on {self.target_url}.

Analyze the following potential security vulnerabilities and risks for admin panels:

1. Authentication & Access Control:
   - Default credentials
   - Weak password policies
   - Missing multi-factor authentication
   - Session management issues
   - Privilege escalation vulnerabilities

2. Input Validation:
   - SQL injection vulnerabilities
   - Cross-site scripting (XSS)
   - Command injection
   - Path traversal attacks

3. Configuration Issues:
   - Exposed admin paths
   - Directory listing enabled
   - Debug mode enabled
   - Unnecessary services running

4. Data Protection:
   - Unencrypted data transmission
   - Sensitive data exposure
   - Insecure direct object references
   - Missing access controls

5. Logging & Monitoring:
   - Insufficient logging
   - Missing audit trails
   - No intrusion detection

Provide a detailed security assessment report in JSON format with the following structure:
{{
    "target_url": "{self.target_url}",
    "scan_type": "admin_panel_security",
    "vulnerabilities": [
        {{
            "id": "vulnerability_id",
            "name": "vulnerability_name",
            "severity": "critical|high|medium|low",
            "description": "detailed description",
            "impact": "potential impact",
            "remediation": "how to fix"
        }}
    ],
    "risk_score": 0-100,
    "recommendations": ["recommendation1", "recommendation2"],
    "summary": "overall assessment summary"
}}

Generate realistic but hypothetical vulnerabilities based on common admin panel security issues."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
            else:
                result = {
                    "target_url": self.target_url,
                    "scan_type": "admin_panel_security",
                    "vulnerabilities": [],
                    "risk_score": 0,
                    "recommendations": [],
                    "summary": response_text,
                    "error": "Could not parse JSON response"
                }
        except json.JSONDecodeError:
            result = {
                "target_url": self.target_url,
                "scan_type": "admin_panel_security",
                "vulnerabilities": [],
                "risk_score": 0,
                "recommendations": [],
                "summary": response_text,
                "error": "JSON parsing failed"
            }
        
        if self.verbose:
            print(f"Admin Panel Security Scan Results for {self.target_url}:")
            print(json.dumps(result, indent=2))
        
        return result