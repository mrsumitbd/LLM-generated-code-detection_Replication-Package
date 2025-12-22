from typing import FrozenSet, Iterable, Optional, Tuple, Union
from packaging.utils import NormalizedName

def format_name(project: NormalizedName, extras: FrozenSet[NormalizedName]) -> str:
    if not extras:
        return project
    extras_expr = ",".join(sorted(extras))
    return f"{project}[{extras_expr}]"