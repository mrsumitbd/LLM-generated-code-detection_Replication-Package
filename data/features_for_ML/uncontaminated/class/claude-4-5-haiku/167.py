import os
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsCompat:
    """Compatibility layer for YAML settings"""

    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser("~/.config/settings.db")
        self.settings = {}
        self.badge_settings = {}
        self._badge_cache = {}

    def _get_yaml_path(self, path=None):
        if path is None:
            path = os.path.expanduser("~/.config/settings.yaml")
        elif not os.path.isabs(path):
            path = os.path.expanduser(f"~/.config/{path}")
        return path

    def load_settings(self, path=None):
        yaml_path = self._get_yaml_path(path)
        
        if os.path.exists(yaml_path):
            try:
                with open(yaml_path, 'r') as f:
                    self.settings = yaml.safe_load(f) or {}
                return self.settings
            except (yaml.YAMLError, IOError) as e:
                print(f"Error loading YAML settings from {yaml_path}: {e}")
                self.settings = {}
        else:
            self.settings = self._load_from_database()
        
        return self.settings

    def _load_from_database(self):
        settings = {}
        
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    if self.db_path.endswith('.json'):
                        settings = json.load(f)
                    else:
                        settings = yaml.safe_load(f) or {}
            except (json.JSONDecodeError, yaml.YAMLError, IOError) as e:
                print(f"Error loading database settings from {self.db_path}: {e}")
                settings = {}
        
        return settings

    def load_badge_settings(self, badge_file, force_reload=False):
        if badge_file in self._badge_cache and not force_reload:
            return self._badge_cache[badge_file]
        
        badge_path = self._get_yaml_path(badge_file)
        badge_data = {}
        
        if os.path.exists(badge_path):
            try:
                with open(badge_path, 'r') as f:
                    badge_data = yaml.safe_load(f) or {}
            except (yaml.YAMLError, IOError) as e:
                print(f"Error loading badge settings from {badge_path}: {e}")
                badge_data = {}
        
        self._badge_cache[badge_file] = badge_data
        self.badge_settings = badge_data
        
        return badge_data