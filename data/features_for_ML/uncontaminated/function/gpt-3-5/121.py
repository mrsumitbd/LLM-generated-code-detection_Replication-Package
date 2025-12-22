def display_as_textured(ref):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    ax.imshow(ref, cmap='viridis', interpolation='nearest')
    ax.axis('off')
    plt.show()