import os
from PIL import Image
import numpy as np

class LowMemoryImageFolder:

    def __init__(self, folder, file_list=None):
        self.folder = folder
        self.file_list = file_list
        
        if file_list is None:
            self.file_list = []
            valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            for filename in sorted(os.listdir(folder)):
                if os.path.splitext(filename)[1].lower() in valid_extensions:
                    self.file_list.append(filename)
        else:
            self.file_list = file_list

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, item):
        if item < 0 or item >= len(self.file_list):
            raise IndexError("Index out of range")
        
        filename = self.file_list[item]
        filepath = os.path.join(self.folder, filename)
        
        try:
            image = Image.open(filepath)
            return np.array(image)
        except Exception as e:
            raise RuntimeError(f"Failed to load image {filepath}: {str(e)}")

    def __del__(self):
        pass