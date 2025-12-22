import matplotlib.pyplot as plt
from typing import List

def get_colorbrewer_scheme(scheme_name: str, n_colors: int = 5) -> List[str]:
    """
    Get ColorBrewer color scheme from matplotlib.

    Args:
        scheme_name: Name of the ColorBrewer scheme (e.g., 'Set1', 'Spectral', 'RdYlBu')
        n_colors: Number of colors to extract

    Returns:
        List of hex color codes
    """
    cmap = plt.get_cmap(scheme_name)
    colors = cmap(range(n_colors))
    return [f'#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}' for c in colors]