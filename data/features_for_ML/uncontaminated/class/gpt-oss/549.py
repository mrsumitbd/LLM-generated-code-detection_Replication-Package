import os
import json
import shutil
import zipfile
import webbrowser
from pathlib import Path
from typing import Optional


class ManualTools:
    """手动操作工具类"""

    def __init__(self):
        self.data_dir = Path.cwd() / "data"
        self.backup_dir = Path.cwd() / "backups"
        self.data_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)

    def collect_data(self, data_type: str = "all", dimension: str = "both") -> bool:
        """Simulate data collection."""
        try:
            file_path = self.data_dir / f"{data_type}_{dimension}.json"
            sample = {"type": data_type, "dimension": dimension, "content": []}
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(sample, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def open_browser(self, page: str = "home", stay_open: bool = True) -> bool:
        """Open a web page in the default browser."""
        try:
            url_map = {
                "home": "https://www.example.com",
                "about": "https://www.example.com/about",
                "contact": "https://www.example.com/contact",
            }
            url = url_map.get(page, url_map["home"])
            webbrowser.open(url, new=2)
            return True
        except Exception:
            return False

    def export_data(self, format: str = "excel", output_dir: Optional[str] = None) -> bool:
        """Export collected data to a file."""
        try:
            out_dir = Path(output_dir) if output_dir else self.data_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            if format.lower() == "excel":
                out_file = out_dir / "export.xlsx"
                out_file.touch()
            elif format.lower() == "csv":
                out_file = out_dir / "export.csv"
                out_file.touch()
            else:
                out_file = out_dir / f"export.{format}"
                out_file.touch()
            return True
        except Exception:
            return False

    def analyze_trends(self) -> bool:
        """Perform a simple trend analysis on collected data."""
        try:
            for file in self.data_dir.glob("*.json"):
                with file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                # Dummy analysis: count entries
                count = len(data.get("content", []))
                print(f"Analyzed {file.name}: {count} entries.")
            return True
        except Exception:
            return False

    def backup_data(self, include_cookies: bool = True) -> bool:
        """Create a backup zip of the data directory."""
        try:
            backup_file = self.backup_dir / f"backup_{self._timestamp()}.zip"
            with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(self.data_dir):
                    for f in files:
                        full_path = Path(root) / f
                        zf.write(full_path, arcname=full_path.relative_to(self.data_dir))
                if include_cookies:
                    cookies_file = Path.cwd() / "cookies.json"
                    if cookies_file.exists():
                        zf.write(cookies_file, arcname="cookies.json")
            return True
        except Exception:
            return False

    def restore_backup(self, backup_path: str) -> bool:
        """Restore data from a backup zip file."""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return False
            with zipfile.ZipFile(backup_file, "r") as zf:
                zf.extractall(self.data_dir)
            return True
        except Exception:
            return False

    @staticmethod
    def _timestamp() -> str:
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")