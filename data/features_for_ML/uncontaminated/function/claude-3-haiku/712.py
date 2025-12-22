import os
import shutil
import tkinter as tk
from tkinter import filedialog

def install_worlds(server_name, base_dir, script_dir):
    """Provides a menu to select and install .mcworld files.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
        script_dir (str): The directory where the script is located.
    Returns:
        int: 0 on success, error code on failure.

    """
    server_path = os.path.join(base_dir, server_name)
    worlds_dir = os.path.join(server_path, "worlds")
    os.makedirs(worlds_dir, exist_ok=True)

    root = tk.Tk()
    root.withdraw()

    mcworld_file = filedialog.askopenfilename(
        title="Select .mcworld file",
        filetypes=[("Minecraft World", "*.mcworld")],
        initialdir=script_dir
    )

    if mcworld_file:
        try:
            with zipfile.ZipFile(mcworld_file, "r") as zip_ref:
                zip_ref.extractall(worlds_dir)
            print(f"World installed successfully in {worlds_dir}")
            return 0
        except Exception as e:
            print(f"Error installing world: {e}")
            return 1
    else:
        print("No .mcworld file selected.")
        return 0