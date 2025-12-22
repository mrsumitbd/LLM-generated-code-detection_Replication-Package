import matplotlib.pyplot as plt

def plot_scale_line(lines, label, ax):
    """
    Plot one or more scale lines on the given matplotlib axis.

    Parameters
    ----------
    lines : list
        A list of line segments. Each segment can be specified in one of two ways:
        1. As a tuple of two points: ((x1, y1), (x2, y2))
        2. As a list/tuple of four numbers: (x1, y1, x2, y2)
        If a single segment is provided, it can be passed directly instead of a list.
    label : str
        Text label to annotate the scale line (e.g., "10 km").
    ax : matplotlib.axes.Axes
        The axis on which to plot the scale line.
    """
    # Normalize input to a list of segments
    if not isinstance(lines, (list, tuple)):
        # Assume a single segment
        lines = [lines]

    # Ensure each segment is in the form ((x1, y1), (x2, y2))
    segments = []
    for seg in lines:
        if isinstance(seg, (list, tuple)):
            if len(seg) == 2:
                # Might be ((x1, y1), (x2, y2))
                p1, p2 = seg
                if isinstance(p1, (list, tuple)) and isinstance(p2, (list, tuple)):
                    segments.append((tuple(p1), tuple(p2)))
                else:
                    raise ValueError(f"Invalid segment format: {seg}")
            elif len(seg) == 4:
                # (x1, y1, x2, y2)
                x1, y1, x2, y2 = seg
                segments.append(((x1, y1), (x2, y2)))
            else:
                raise ValueError(f"Segment must have 2 or 4 elements: {seg}")
        else:
            raise ValueError(f"Segment must be a list or tuple: {seg}")

    # Plot each segment
    for (x1, y1), (x2, y2) in segments:
        ax.plot([x1, x2], [y1, y2], color='k', linewidth=2)

        # Draw tick marks at the ends
        # Determine a small offset perpendicular to the line
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            continue
        # Normalized perpendicular vector
        nx = -dy / length
        ny = dx / length
        tick_len = 0.02 * length  # 2% of line length
        # Start tick
        ax.plot([x1, x1 + nx * tick_len], [y1, y1 + ny * tick_len], color='k', linewidth=2)
        # End tick
        ax.plot([x2, x2 + nx * tick_len], [y2, y2 + ny * tick_len], color='k', linewidth=2)

        # Place label at the midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        # Offset label slightly along the perpendicular direction
        label_offset = 0.05 * length
        ax.text(mid_x + nx * label_offset,
                mid_y + ny * label_offset,
                label,
                ha='center',
                va='center',
                fontsize=10,
                color='k',
                backgroundcolor='white',
                bbox=dict(facecolor='white', edgecolor='none', pad=0.2))

    # Ensure the scale line is visible
    ax.autoscale_view()