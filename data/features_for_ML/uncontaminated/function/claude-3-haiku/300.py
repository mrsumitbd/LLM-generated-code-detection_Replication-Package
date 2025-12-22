import os
import shutil
from pathlib import Path
from typing import Namespace

def import_command(args: Namespace) -> None:
    source_dir = Path(args.source)
    destination_dir = Path(args.destination)

    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    if not destination_dir.exists():
        os.makedirs(destination_dir, exist_ok=True)

    for item in source_dir.glob('*'):
        if item.is_file():
            destination_file = destination_dir / item.name
            shutil.copy2(item, destination_file)
            print(f"Copied '{item.name}' to '{destination_dir}'.")
        elif item.is_dir():
            destination_subdir = destination_dir / item.name
            shutil.copytree(item, destination_subdir)
            print(f"Copied directory '{item.name}' to '{destination_dir}'.")