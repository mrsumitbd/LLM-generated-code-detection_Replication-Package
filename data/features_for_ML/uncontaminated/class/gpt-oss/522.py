import os
from pathlib import Path
from PIL import Image
import glob

class LowMemoryImageFolder:
    """
    A lightweight image folder loader that loads images on demand.
    """

    def __init__(self, folder, file_list=None):
        """
        Parameters
        ----------
        folder : str or Path
            Path to the image folder.
        file_list : list of str, optional
            List of image file names (relative to folder). If None, all image files
            in the folder will be used.
        """
        self.folder = Path(folder)
        if not self.folder.is_dir():
            raise ValueError(f"Provided folder {folder} is not a directory")

        if file_list is None:
            # Use common image extensions
            patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.gif"]
            files = []
            for pattern in patterns:
                files.extend(glob.glob(str(self.folder / pattern)))
            self.file_list = sorted(files)
        else:
            # Resolve relative paths
            self.file_list = [str(self.folder / f) for f in file_list]

        self._len = len(self.file_list)

    def __len__(self):
        return self._len

    def __getitem__(self, idx):
        """
        Load the image at the given index.

        Returns
        -------
        PIL.Image.Image
            The loaded image.
        """
        if idx < 0 or idx >= self._len:
            raise IndexError(f"Index {idx} out of range for dataset of size {self._len}")

        img_path = self.file_list[idx]
        with Image.open(img_path) as img:
            # Load the image into memory and close the file
            img_converted = img.convert("RGB")
            return img_converted.copy()

    def __del__(self):
        # No explicit resources to clean up
        pass