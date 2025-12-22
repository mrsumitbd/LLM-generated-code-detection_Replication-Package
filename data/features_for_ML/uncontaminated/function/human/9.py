from typing import Any, Dict, List, Optional
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def get_colorbrewer_scheme(scheme_name: str, n_colors: int = 5) -> List[str]:
    """
    Get ColorBrewer color scheme from matplotlib.

    Args:
        scheme_name: Name of the ColorBrewer scheme (e.g., 'Set1', 'Spectral', 'RdYlBu')
        n_colors: Number of colors to extract

    Returns:
        List of hex color codes
    """
    if not MATPLOTLIB_AVAILABLE:
        return []

    # Map common lowercase names to proper matplotlib names
    scheme_map = {
        "set1": "Set1",
        "set2": "Set2",
        "set3": "Set3",
        "spectral": "Spectral",
        "rdylbu": "RdYlBu",
        "rdylgn": "RdYlGn",
        "paired": "Paired",
        "dark2": "Dark2",
        "accent": "Accent",
        "pastel1": "Pastel1",
        "pastel2": "Pastel2",
        "rdbu": "RdBu",
        "rdgy": "RdGy",
        "rdpu": "RdPu",
        "bugn": "BuGn",
        "bupu": "BuPu",
        "gnbu": "GnBu",
        "orrd": "OrRd",
        "pubugn": "PuBuGn",
        "pubu": "PuBu",
        "purd": "PuRd",
        "ylgn": "YlGn",
        "ylgnbu": "YlGnBu",
        "ylorbr": "YlOrBr",
        "ylorrd": "YlOrRd",
    }

    # Normalize scheme name
    scheme_lower = scheme_name.lower()
    actual_scheme = scheme_map.get(scheme_lower, scheme_name)

    try:
        cmap = plt.get_cmap(actual_scheme)
        colors = []
        for i in range(n_colors):
            rgba = cmap(i / (n_colors - 1) if n_colors > 1 else 0.5)
            colors.append(mcolors.rgb2hex(rgba[:3]))
        return colors
    except Exception as e:
        logger.warning(f"Could not get ColorBrewer scheme '{scheme_name}': {e}")
        return []