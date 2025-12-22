from typing import (
    Dict, Any, Type, Optional, Callable, List, Union
)

class ComputedBindingConfig:
    """Configuration for computed reactive bindings"""

    compute_fn: Callable[[], Any]
    dependencies: List[str]  # Names of reactive attributes
    transform: Optional[Callable[[Any], Any]] = None
    on_change: Optional[Callable[[Any, Any], None]] = None