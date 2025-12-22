import matplotlib.pyplot as plt

def plot_scale_line(lines, label, ax):
    """
    Plots a scale line on the given axis.

    Args:
        lines (list): A list of line objects to which the scale line should be added.
        label (str): The label for the scale line.
        ax (matplotlib.axes.Axes): The axis on which the scale line should be plotted.
    """
    # Get the x-limits of the axis
    x_min, x_max = ax.get_xlim()

    # Calculate the length of the scale line
    scale_length = (x_max - x_min) * 0.1

    # Plot the scale line
    ax.plot([x_min, x_min + scale_length], [0, 0], '-', color='black', linewidth=2)

    # Add the label
    ax.text(x_min + scale_length / 2, 0, label, ha='center', va='top')

    # Add the line objects to the list
    lines.append(ax.lines[-1])