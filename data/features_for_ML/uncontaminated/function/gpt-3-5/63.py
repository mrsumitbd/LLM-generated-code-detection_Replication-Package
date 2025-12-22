def save_tensor_to_img(tensor, save_dir):
    import matplotlib.pyplot as plt
    import numpy as np

    if isinstance(tensor, np.ndarray):
        img = tensor
    else:
        img = tensor.numpy()

    plt.imsave(save_dir, img)