class PluginFileChecker:
    """Checks Discourse plugin files for security and integrity issues"""

    def __init__(self, scanner):
        self.scanner = scanner
        self.plugin_registry = {}
        self.security_issues = []

    def check_plugin_files(self):
        """Main method to check all plugin files"""
        try:
            # Get plugin list from Discourse
            url = f"{self.scanner.base_url}/admin/plugins.json"
            response = self.scanner.session.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.json()
                plugin_names = self._extract_plugin_names(content)
                
                for plugin_name in plugin_names:
                    self._check_individual_plugin(plugin_name)
                
                return {
                    'status': 'completed',
                    'plugins_checked': len(plugin_names),
                    'issues_found': len(self.security_issues),
                    'issues': self.security_issues
                }
            else:
                return {
                    'status': 'failed',
                    'error': f'Failed to retrieve plugins: {response.status_code}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _extract_plugin_names(self, content):
        """Extract plugin names from API response"""
        plugin_names = []
        
        if isinstance(content, dict):
            if 'plugins' in content:
                plugins = content['plugins']
                if isinstance(plugins, list):
                    for plugin in plugins:
                        if isinstance(plugin, dict) and 'name' in plugin:
                            plugin_names.append(plugin['name'])
                        elif isinstance(plugin, str):
                            plugin_names.append(plugin)
        
        return plugin_names

    def _check_individual_plugin(self, plugin_name):
        """Check individual plugin for security issues"""
        try:
            # Check plugin metadata
            url = f"{self.scanner.base_url}/admin/plugins/{plugin_name}.json"
            response = self.scanner.session.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.json()
                self._check_plugin_content(plugin_name, content, url)
            else:
                self.security_issues.append({
                    'plugin': plugin_name,
                    'issue': 'Unable to retrieve plugin information',
                    'severity': 'medium'
                })
        except Exception as e:
            self.security_issues.append({
                'plugin': plugin_name,
                'issue': f'Error checking plugin: {str(e)}',
                'severity': 'low'
            })

    def _check_plugin_content(self, plugin_name, content, url):
        """Check plugin content for security and integrity issues"""
        issues = []
        
        # Check for missing or invalid metadata
        if not isinstance(content, dict):
            issues.append({
                'type': 'invalid_format',
                'description': 'Plugin metadata is not in valid format'
            })
            return
        
        # Check for required fields
        required_fields = ['name', 'version']
        for field in required_fields:
            if field not in content:
                issues.append({
                    'type': 'missing_field',
                    'description': f'Missing required field: {field}'
                })
        
        # Check for suspicious permissions or capabilities
        if 'permissions' in content:
            permissions = content['permissions']
            dangerous_permissions = ['admin', 'root', 'system']
            for perm in dangerous_permissions:
                if perm in str(permissions).lower():
                    issues.append({
                        'type': 'dangerous_permission',
                        'description': f'Plugin requests dangerous permission: {perm}',
                        'severity': 'high'
                    })
        
        # Check for outdated versions
        if 'version' in content:
            version = content['version']
            if version and len(str(version).split('.')) < 2:
                issues.append({
                    'type': 'version_format',
                    'description': 'Plugin version format appears invalid'
                })
        
        # Check for enabled status
        if 'enabled' in content:
            if not content['enabled']:
                issues.append({
                    'type': 'disabled_plugin',
                    'description': 'Plugin is currently disabled',
                    'severity': 'low'
                })
        
        # Add issues to the main list
        for issue in issues:
            self.security_issues.append({
                'plugin': plugin_name,
                'issue': issue['description'],
                'type': issue.get('type', 'unknown'),
                'severity': issue.get('severity', 'medium')
            })