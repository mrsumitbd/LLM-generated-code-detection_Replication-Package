import os
import importlib

def import_extensions():
    extensions_dir = os.path.join(os.path.dirname(__file__), 'extensions')
    if not os.path.exists(extensions_dir):
        return

    for filename in os.listdir(extensions_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = os.path.splitext(filename)[0]
            module_path = os.path.join(extensions_dir, filename)
            try:
                importlib.import_module(f'extensions.{module_name}')
            except Exception as e:
                print(f"Error importing extension '{module_name}': {e}")