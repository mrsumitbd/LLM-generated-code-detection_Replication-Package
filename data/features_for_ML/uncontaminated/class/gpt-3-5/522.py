import os
from PIL import Image
from torch.utils.data import Dataset

class LowMemoryImageFolder(Dataset):

    def __init__(self, folder, file_list=None):
        self.folder = folder
        if file_list is None:
            self.file_list = os.listdir(folder)
        else:
            self.file_list = file_list

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, item):
        file_name = self.file_list[item]
        image_path = os.path.join(self.folder, file_name)
        image = Image.open(image_path)
        return image

    def __del__(self):
        pass