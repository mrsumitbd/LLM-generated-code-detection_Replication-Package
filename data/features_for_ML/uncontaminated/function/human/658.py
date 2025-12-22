from typing import Any, Dict, AsyncGenerator, Optional, Tuple, Union

def get_setting(tab: str, key: str, default: Any = None):
            comp = webui_manager.id_to_component.get(f"{tab}.{key}")
            return components.get(comp, default) if comp else default