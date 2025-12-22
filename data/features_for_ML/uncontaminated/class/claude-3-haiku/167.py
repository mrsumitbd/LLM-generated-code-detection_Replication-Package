import os
import yaml
import sqlite3

class SettingsCompat:
    """Compatibility layer for YAML settings"""

    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'settings.db')
        self.settings = None

    def _get_yaml_path(self, path=None):
        if path is None:
            return os.path.join(os.path.dirname(__file__), 'settings.yml')
        return path

    def load_settings(self, path=None):
        yaml_path = self._get_yaml_path(path)
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                self.settings = yaml.safe_load(f)
        else:
            self._load_from_database()

    def _load_from_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT settings FROM settings')
        result = c.fetchone()
        if result:
            self.settings = yaml.safe_load(result[0])
        conn.close()

    def load_badge_settings(self, badge_file, force_reload=False):
        if self.settings is None or force_reload:
            self.load_settings()

        badge_path = os.path.join(os.path.dirname(__file__), badge_file)
        with open(badge_path, 'r') as f:
            badge_settings = yaml.safe_load(f)

        self.settings['badges'] = badge_settings