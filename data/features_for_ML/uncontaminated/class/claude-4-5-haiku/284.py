class APIModule:
    """API security module (Refactored)"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.results = {
            "api_access": [],
            "api_keys": [],
            "rate_limiting": []
        }
        self.common_api_endpoints = [
            "/api/v1/",
            "/api/v2/",
            "/api/",
            "/rest/api/",
            "/graphql",
            "/api/graphql"
        ]
        self.common_api_keys = [
            "api_key",
            "apikey",
            "api-key",
            "x-api-key",
            "authorization",
            "bearer",
            "token",
            "access_token",
            "secret_key",
            "client_id",
            "client_secret"
        ]

    def run(self) -> Dict[str, Any]:
        """Run all API security tests"""
        self._test_api_access()
        self._test_api_keys()
        self._test_rate_limiting()
        
        return {
            "module": "API Security",
            "tests": self.results,
            "summary": {
                "total_issues": sum(len(v) for v in self.results.values()),
                "access_issues": len(self.results["api_access"]),
                "key_issues": len(self.results["api_keys"]),
                "rate_limit_issues": len(self.results["rate_limiting"])
            }
        }

    def _test_api_access(self):
        """Test for insecure API access patterns"""
        issues = []
        
        # Check for unencrypted API endpoints
        if hasattr(self.scanner, 'target_url'):
            if self.scanner.target_url.startswith('http://'):
                issues.append({
                    "severity": "HIGH",
                    "type": "Unencrypted API",
                    "description": "API endpoint uses HTTP instead of HTTPS",
                    "url": self.scanner.target_url
                })
        
        # Check for missing authentication
        for endpoint in self.common_api_endpoints:
            if hasattr(self.scanner, 'check_endpoint'):
                result = self.scanner.check_endpoint(endpoint)
                if result and not result.get('requires_auth', True):
                    issues.append({
                        "severity": "HIGH",
                        "type": "Missing Authentication",
                        "description": f"API endpoint {endpoint} does not require authentication",
                        "endpoint": endpoint
                    })
        
        # Check for CORS misconfiguration
        if hasattr(self.scanner, 'headers'):
            cors_header = self.scanner.headers.get('Access-Control-Allow-Origin', '')
            if cors_header == '*':
                issues.append({
                    "severity": "MEDIUM",
                    "type": "CORS Misconfiguration",
                    "description": "CORS allows requests from any origin",
                    "header": cors_header
                })
        
        self.results["api_access"] = issues

    def _test_api_keys(self):
        """Test for exposed or weak API keys"""
        issues = []
        
        # Check for hardcoded API keys in common locations
        if hasattr(self.scanner, 'source_code'):
            for key_name in self.common_api_keys:
                if key_name in self.scanner.source_code.lower():
                    # Check if followed by actual key value
                    patterns = [
                        f'{key_name}=',
                        f'{key_name}:',
                        f'"{key_name}"',
                        f"'{key_name}'"
                    ]
                    for pattern in patterns:
                        if pattern in self.scanner.source_code.lower():
                            issues.append({
                                "severity": "CRITICAL",
                                "type": "Exposed API Key",
                                "description": f"Potential hardcoded API key found: {key_name}",
                                "key_name": key_name
                            })
                            break
        
        # Check for weak API key generation
        if hasattr(self.scanner, 'api_keys'):
            for key in self.scanner.api_keys:
                if len(key) < 32:
                    issues.append({
                        "severity": "HIGH",
                        "type": "Weak API Key",
                        "description": "API key is too short (less than 32 characters)",
                        "key_length": len(key)
                    })
        
        # Check for API keys in URLs
        if hasattr(self.scanner, 'target_url'):
            if '?' in self.scanner.target_url and any(k in self.scanner.target_url.lower() for k in self.common_api_keys):
                issues.append({
                    "severity": "HIGH",
                    "type": "API Key in URL",
                    "description": "API key exposed in URL parameters",
                    "url": self.scanner.target_url
                })
        
        self.results["api_keys"] = issues

    def _test_rate_limiting(self):
        """Test for rate limiting implementation"""
        issues = []
        
        # Check for rate limit headers
        if hasattr(self.scanner, 'headers'):
            rate_limit_headers = [
                'X-RateLimit-Limit',
                'X-RateLimit-Remaining',
                'X-RateLimit-Reset',
                'RateLimit-Limit',
                'RateLimit-Remaining'
            ]
            
            found_headers = [h for h in rate_limit_headers if h in self.scanner.headers]
            
            if not found_headers:
                issues.append({
                    "severity": "MEDIUM",
                    "type": "Missing Rate Limiting Headers",
                    "description": "API does not return rate limiting information in headers"
                })
        
        # Check for rate limit enforcement
        if hasattr(self.scanner, 'check_rate_limit'):
            if not self.scanner.check_rate_limit():
                issues.append({
                    "severity": "HIGH",
                    "type": "No Rate Limiting",
                    "description": "API does not enforce rate limiting",
                    "risk": "Vulnerable to brute force and DoS attacks"
                })
        
        # Check for reasonable rate limits
        if hasattr(self.scanner, 'headers'):
            limit = self.scanner.headers.get('X-RateLimit-Limit')
            if limit and int(limit) > 10000:
                issues.append({
                    "severity": "LOW",
                    "type": "Permissive Rate Limit",
                    "description": "Rate limit is very high, may not provide adequate protection",
                    "limit": limit
                })
        
        self.results["rate_limiting"] = issues