from PIL import Image
import numpy as np

def save_tensor_to_img(tensor, save_dir):
    from PIL import Image
    import numpy as np
    for idx, img in enumerate(tensor):
        img = img[..., :3].cpu().numpy()
        img = (img * 255).astype(np.uint8)
        img = Image.fromarray(img)
        img.save(save_dir + f"{idx}.png")