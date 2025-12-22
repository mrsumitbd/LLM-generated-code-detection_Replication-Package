from typing import Callable, Dict, Optional, List, Any, get_type_hints

def decorator(func: Callable):
            resource_name = name or uri
            resource_description = description or func.__doc__ or f"Resource: {uri}"

            self.resources[uri] = ResourceMetadata(
                func=func,
                uri=uri,
                name=resource_name,
                description=resource_description.strip(),
                mime_type=mime_type,
            )
            return func