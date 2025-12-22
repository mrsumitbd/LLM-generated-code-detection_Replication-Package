import os
from PIL import Image

class LowMemoryImageFolder:
    def __init__(self, folder, file_list=None):
        self.folder = folder
        if file_list is None:
            self.file_list = os.listdir(folder)
        else:
            self.file_list = file_list
        self.file_paths = [os.path.join(folder, f) for f in self.file_list]

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, item):
        file_path = self.file_paths[item]
        return Image.open(file_path)

    def __del__(self):
        for file_path in self.file_paths:
            try:
                os.remove(file_path)
            except OSError:
                pass