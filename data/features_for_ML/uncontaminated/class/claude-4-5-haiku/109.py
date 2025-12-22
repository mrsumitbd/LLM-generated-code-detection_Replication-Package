class AssetFileChecker:
    """Checks asset files for security vulnerabilities and malicious content"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.issues = []
        self.asset_files = {}
        self.javascript_endpoints = set()
        self.robots_entries = []
        self.sitemap_entries = []

    def run(self):
        """Execute all asset file checks"""
        self.check_asset_files()
        self.analyze_javascript_endpoints()
        self.analyze_discourse_robots_sitemap()
        return self._generate_summary()

    def check_asset_files(self):
        """Check all asset files for vulnerabilities"""
        if not hasattr(self.scanner, 'response') or not self.scanner.response:
            return

        content = self.scanner.response.text
        base_path = self.scanner.url

        self._extract_asset_files(content, base_path)

        for asset_file, asset_data in self.asset_files.items():
            self._check_asset_file(asset_data)

    def _extract_asset_files(self, content, base_path):
        """Extract asset file references from HTML content"""
        import re

        # Extract script tags
        script_pattern = r'<script[^>]*src=["\']([^"\']+)["\']'
        for match in re.finditer(script_pattern, content):
            url = match.group(1)
            self.asset_files[url] = {
                'type': 'script',
                'url': url,
                'content': None
            }

        # Extract link tags (stylesheets)
        link_pattern = r'<link[^>]*href=["\']([^"\']+)["\']'
        for match in re.finditer(link_pattern, content):
            url = match.group(1)
            self.asset_files[url] = {
                'type': 'stylesheet',
                'url': url,
                'content': None
            }

        # Extract img tags
        img_pattern = r'<img[^>]*src=["\']([^"\']+)["\']'
        for match in re.finditer(img_pattern, content):
            url = match.group(1)
            self.asset_files[url] = {
                'type': 'image',
                'url': url,
                'content': None
            }

    def _check_asset_content(self, asset_file, content, url):
        """Check asset content for malicious patterns"""
        malicious_patterns = [
            r'eval\s*\(',
            r'document\.write',
            r'innerHTML\s*=',
            r'<iframe',
            r'onclick\s*=',
            r'onerror\s*=',
            r'onload\s*=',
            r'fetch\s*\(',
            r'XMLHttpRequest',
            r'crypto-miner',
            r'bitcoin',
            r'monero'
        ]

        import re
        for pattern in malicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.issues.append({
                    'type': 'malicious_content',
                    'severity': 'high',
                    'asset': url,
                    'pattern': pattern,
                    'message': f'Potentially malicious pattern detected in {asset_file}: {pattern}'
                })

    def _check_asset_file(self, asset_file):
        """Check individual asset file for issues"""
        url = asset_file.get('url', '')
        asset_type = asset_file.get('type', '')

        # Check for missing integrity attributes
        if asset_type in ['script', 'stylesheet']:
            self.issues.append({
                'type': 'missing_integrity',
                'severity': 'medium',
                'asset': url,
                'message': f'Asset {url} missing integrity attribute'
            })

        # Check for HTTP instead of HTTPS
        if url.startswith('http://'):
            self.issues.append({
                'type': 'insecure_protocol',
                'severity': 'high',
                'asset': url,
                'message': f'Asset {url} uses insecure HTTP protocol'
            })

        # Check for suspicious file extensions
        suspicious_extensions = ['.exe', '.dll', '.bat', '.cmd', '.sh']
        if any(url.lower().endswith(ext) for ext in suspicious_extensions):
            self.issues.append({
                'type': 'suspicious_extension',
                'severity': 'high',
                'asset': url,
                'message': f'Asset {url} has suspicious file extension'
            })

    def get_asset_security_summary(self, all_issues):
        """Generate security summary for assets"""
        asset_issues = [issue for issue in all_issues if 'asset' in issue]

        high_severity = len([i for i in asset_issues if i.get('severity') == 'high'])
        medium_severity = len([i for i in asset_issues if i.get('severity') == 'medium'])
        low_severity = len([i for i in asset_issues if i.get('severity') == 'low'])

        return {
            'total_assets': len(self.asset_files),
            'total_issues': len(asset_issues),
            'high_severity': high_severity,
            'medium_severity': medium_severity,
            'low_severity': low_severity,
            'issues': asset_issues
        }

    def analyze_javascript_endpoints(self):
        """Analyze JavaScript endpoints for security issues"""
        for asset_url in self.asset_files:
            if asset_url.endswith('.js'):
                self.javascript_endpoints.add(asset_url)

        if not self.javascript_endpoints:
            self.issues.append({
                'type': 'info',
                'severity': 'info',
                'message': 'No JavaScript endpoints found'
            })

    def analyze_discourse_robots_sitemap(self):
        """Analyze robots.txt and sitemap.xml for information disclosure"""
        robots_url = self.scanner.url.rstrip('/') + '/robots.txt'
        sitemap_url = self.scanner.url.rstrip('/') + '/sitemap.xml'

        try:
            import requests
            robots_response = requests.get(robots_url, timeout=5)
            if robots_response.status_code == 200:
                self.robots_entries = robots_response.text.split('\n')
                self.issues.append({
                    'type': 'info_disclosure',
                    'severity': 'low',
                    'message': f'robots.txt found at {robots_url}',
                    'entries': len(self.robots_entries)
                })
        except:
            pass

        try:
            import requests
            sitemap_response = requests.get(sitemap_url, timeout=5)
            if sitemap_response.status_code == 200:
                self.sitemap_entries = sitemap_response.text.split('\n')
                self.issues.append({
                    'type': 'info_disclosure',
                    'severity': 'low',
                    'message': f'sitemap.xml found at {sitemap_url}',
                    'entries': len(self.sitemap_entries)
                })
        except:
            pass

    def _generate_summary(self):
        """Generate final security summary"""
        return {
            'asset_files_checked': len(self.asset_files),
            'javascript_endpoints': len(self.javascript_endpoints),
            'total_issues': len(self.issues),
            'issues': self.issues,
            'robots_txt_found': len(self.robots_entries) > 0,
            'sitemap_xml_found': len(self.sitemap_entries) > 0
        }