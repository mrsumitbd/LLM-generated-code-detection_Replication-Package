from matplotlib.patches import Patch, Polygon

def plot_scale_line(lines, label, ax):
    for i, line in enumerate(lines):
        x1, y1, x2, y2 = points2(line)
        ax.add_patch(Polygon([(x1, y1), (x2, y2)], facecolor="gray", edgecolor="none", lw=2))
        if i >= 1:
            ax.text(float(x1), float(y1) - 20, label[i - 1], va="bottom", ha="center")