def get_colorbrewer_scheme(scheme_name: str, n_colors: int = 5) -> List[str]:
    """
    Get ColorBrewer color scheme from matplotlib.

    Args:
        scheme_name: Name of the ColorBrewer scheme (e.g., 'Set1', 'Spectral', 'RdYlBu')
        n_colors: Number of colors to extract

    Returns:
        List of hex color codes
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import rgb2hex
    
    # Clamp n_colors to valid range (3-12 for most ColorBrewer schemes)
    n_colors = max(3, min(n_colors, 12))
    
    try:
        # Get the colormap from matplotlib
        cmap = plt.cm.get_cmap(f'{scheme_name}')
        
        # Sample n_colors evenly from the colormap
        colors = [cmap(i / (n_colors - 1)) for i in range(n_colors)]
        
        # Convert RGBA tuples to hex color codes
        hex_colors = [rgb2hex(color[:3]) for color in colors]
        
        return hex_colors
    except (ValueError, AttributeError):
        # Fallback: try using brewer palettes if available
        try:
            import seaborn as sns
            palette = sns.color_palette(scheme_name, n_colors=n_colors)
            hex_colors = [rgb2hex(color) for color in palette]
            return hex_colors
        except:
            # Default fallback palette
            default_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                             '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                             '#aec7e8', '#ffbb78']
            return default_palette[:n_colors]