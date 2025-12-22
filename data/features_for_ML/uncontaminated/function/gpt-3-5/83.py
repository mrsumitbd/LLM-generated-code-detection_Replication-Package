def plot_scale_line(lines, label, ax):
    for line in lines:
        ax.plot(line[0], line[1], label=label)
    ax.legend()