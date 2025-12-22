from matplotlib import cm
from typing import List

def get_colorbrewer_scheme(scheme_name: str, n_colors: int = 5) -> List[str]:
    colors = getattr(cm, scheme_name, None)
    if colors is None:
        raise ValueError(f"ColorBrewer scheme '{scheme_name}' not found")

    return [colors(i / n_colors) for i in range(n_colors)]