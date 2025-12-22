import imageio, os
from PIL import Image

class LowMemoryImageFolder:
    def __init__(self, folder, file_list=None):
        if file_list is None:
            self.file_list = search_for_images(folder)
        else:
            self.file_list = [os.path.join(folder, file_name) for file_name in file_list]
    
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, item):
        return Image.open(self.file_list[item]).convert("RGB")

    def __del__(self):
        pass