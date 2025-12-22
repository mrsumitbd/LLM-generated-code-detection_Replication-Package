import os
import sqlite3
import yaml


class SettingsCompat:
    """Compatibility layer for YAML settings"""

    def __init__(self, db_path=None):
        """
        Initialize the settings compatibility layer.

        Parameters
        ----------
        db_path : str, optional
            Path to the SQLite database containing settings. If provided,
            settings will be loaded from the database when a YAML file is
            not found.
        """
        self.db_path = db_path
        self.settings = {}
        self._badge_cache = {}

    def _get_yaml_path(self, path=None):
        """
        Resolve the path to the YAML settings file.

        Parameters
        ----------
        path : str, optional
            Explicit path to the YAML file. If not provided, a default
            location is used.

        Returns
        -------
        str
            The resolved file path.
        """
        if path:
            return path

        # Default to 'settings.yaml' in the same directory as the DB
        if self.db_path:
            dirpath = os.path.dirname(os.path.abspath(self.db_path))
            return os.path.join(dirpath, "settings.yaml")

        # Fallback to the current working directory
        return os.path.join(os.getcwd(), "settings.yaml")

    def load_settings(self, path=None):
        """
        Load settings from a YAML file or, if not found, from the database.

        Parameters
        ----------
        path : str, optional
            Explicit path to the YAML file. If omitted, the default path
            is used.

        Returns
        -------
        dict
            The loaded settings.
        """
        yaml_path = self._get_yaml_path(path)

        if os.path.exists(yaml_path):
            with open(yaml_path, "r", encoding="utf-8") as f:
                self.settings = yaml.safe_load(f) or {}
        else:
            # Fallback to database if available
            if self.db_path:
                self._load_from_database()
            else:
                self.settings = {}

        return self.settings

    def _load_from_database(self):
        """
        Load settings from the SQLite database.

        The database is expected to have a table named `settings` with
        columns `key` and `value`. The `value` column is assumed to be a
        YAML string.
        """
        if not self.db_path or not os.path.exists(self.db_path):
            self.settings = {}
            return

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        try:
            cur.execute("SELECT key, value FROM settings")
            rows = cur.fetchall()
            self.settings = {
                k: yaml.safe_load(v) if isinstance(v, str) else v for k, v in rows
            }
        except sqlite3.Error:
            self.settings = {}
        finally:
            conn.close()

    def load_badge_settings(self, badge_file, force_reload=False):
        """
        Load badge-specific settings from a YAML file.

        Parameters
        ----------
        badge_file : str
            Path to the badge YAML file.
        force_reload : bool, default False
            If True, reload the file even if it was previously cached.

        Returns
        -------
        dict
            The loaded badge settings.
        """
        if not force_reload and badge_file in self._badge_cache:
            return self._badge_cache[badge_file]

        if not os.path.exists(badge_file):
            return {}

        with open(badge_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        self._badge_cache[badge_file] = data
        return data