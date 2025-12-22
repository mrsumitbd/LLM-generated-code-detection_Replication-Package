import os
import sys
import importlib.util
from pathlib import Path

def import_extensions():
    """
    Dynamically import all Python modules from the 'extensions' directory.
    This function discovers and imports all .py files in the extensions folder.
    """
    # Get the directory where this script is located
    current_dir = Path(__file__).parent
    extensions_dir = current_dir / "extensions"
    
    # Check if extensions directory exists
    if not extensions_dir.exists():
        return
    
    # Iterate through all Python files in the extensions directory
    for file_path in extensions_dir.glob("*.py"):
        # Skip __init__.py and __pycache__
        if file_path.name.startswith("__"):
            continue
        
        # Create module name from filename
        module_name = file_path.stem
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)