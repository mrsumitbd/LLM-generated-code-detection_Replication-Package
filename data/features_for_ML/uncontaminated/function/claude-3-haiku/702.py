import os
import json
from pathlib import Path

def set_theme():
    # Get username handling bypass modes
    home_dir = str(Path.home())
    config_file = os.path.join(home_dir, ".config", "theme.json")

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
        theme = config.get("theme", "default")
    else:
        theme = "default"

    os.environ["GTK_THEME"] = theme