def plot_scale_line(lines, label, ax):
    """
    Plot scale lines on a matplotlib axis.
    
    Parameters:
    lines : list of tuples
        Each tuple contains (x_start, y_start, x_end, y_end) coordinates
    label : str
        Label for the scale line
    ax : matplotlib.axes.Axes
        The axes object to plot on
    """
    for line in lines:
        x_start, y_start, x_end, y_end = line
        ax.plot([x_start, x_end], [y_start, y_end], 'k-', linewidth=2)
    
    if lines:
        x_start, y_start, x_end, y_end = lines[0]
        mid_x = (x_start + x_end) / 2
        mid_y = (y_start + y_end) / 2
        ax.text(mid_x, mid_y - 0.5, label, ha='center', va='top', fontsize=10)