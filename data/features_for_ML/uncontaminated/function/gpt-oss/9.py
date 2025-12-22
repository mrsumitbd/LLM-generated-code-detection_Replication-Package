from typing import List
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

def get_colorbrewer_scheme(scheme_name: str, n_colors: int = 5) -> List[str]:
    """
    Get ColorBrewer color scheme from matplotlib.

    Args:
        scheme_name: Name of the ColorBrewer scheme (e.g., 'Set1', 'Spectral', 'RdYlBu')
        n_colors: Number of colors to extract

    Returns:
        List of hex color codes
    """
    if n_colors <= 0:
        raise ValueError("n_colors must be a positive integer")

    cmap = plt.get_cmap(scheme_name)
    if cmap is None:
        raise ValueError(f"Color map '{scheme_name}' not found in matplotlib")

    # If the colormap has discrete colors, use them directly
    if hasattr(cmap, "colors") and cmap.colors is not None:
        colors = cmap.colors
        if n_colors > len(colors):
            raise ValueError(
                f"Requested {n_colors} colors, but the colormap '{scheme_name}' only has {len(colors)} discrete colors"
            )
        hex_colors = [mcolors.to_hex(c) for c in colors[:n_colors]]
        return hex_colors

    # For continuous colormaps, sample evenly spaced values
    # Use endpoint=False to avoid duplicate colors at the end
    positions = np.linspace(0, 1, n_colors, endpoint=False)
    rgba = cmap(positions)
    hex_colors = [mcolors.to_hex(c) for c in rgba]
    return hex_colors