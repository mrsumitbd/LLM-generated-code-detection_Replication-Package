import json
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
import anthropic


class WebhookSecurityModule:
    """Webhook security testing"""

    def __init__(self, target_url: str, session: Optional[Any] = None, verbose: bool = False):
        self.target_url = target_url
        self.session = session
        self.verbose = verbose
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def scan(self) -> Dict[str, Any]:
        """Scan webhook for security vulnerabilities using Claude AI"""
        
        # Prepare the webhook security analysis prompt
        analysis_prompt = f"""Analyze the following webhook URL for security vulnerabilities and best practices:

Webhook URL: {self.target_url}

Please provide a comprehensive security analysis including:
1. URL structure validation
2. HTTPS/TLS requirements
3. Authentication mechanisms
4. Rate limiting considerations
5. Payload validation requirements
6. Signature verification recommendations
7. Potential attack vectors
8. Security best practices
9. Compliance considerations
10. Risk assessment

Format your response as a JSON object with the following structure:
{{
    "url_analysis": {{}},
    "security_issues": [],
    "recommendations": [],
    "risk_level": "low|medium|high|critical",
    "compliance_notes": [],
    "best_practices": []
}}"""

        if self.verbose:
            print(f"Analyzing webhook: {self.target_url}")
            print("Sending analysis request to Claude...")

        # Use Claude to analyze the webhook security
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )

        # Extract the response
        response_text = message.content[0].text

        # Parse the JSON response
        try:
            # Find JSON content in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                analysis_result = json.loads(json_str)
            else:
                analysis_result = {"raw_analysis": response_text}
        except json.JSONDecodeError:
            analysis_result = {"raw_analysis": response_text}

        # Add metadata to the result
        result = {
            "target_url": self.target_url,
            "scan_timestamp": time.time(),
            "analysis": analysis_result,
            "model_used": self.model
        }

        if self.verbose:
            print("Webhook security analysis completed")
            print(f"Risk Level: {analysis_result.get('risk_level', 'unknown')}")

        return result