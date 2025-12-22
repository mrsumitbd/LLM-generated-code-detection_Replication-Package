import os
import numpy as np
import torch
from torch.utils.data import DataLoader
from ebsynth.dataset import EBSynthDataset
from ebsynth.model import EBSynthModel
from ebsynth.utils import save_images

class FastModeRunner:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = EBSynthModel().to(self.device)

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config, save_path=None):
        dataset = EBSynthDataset(frames_guide, frames_style, window_size, ebsynth_config)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)

        self.model.eval()
        with torch.no_grad():
            for batch in dataloader:
                guide_images, style_images = batch
                guide_images = guide_images.to(self.device)
                style_images = style_images.to(self.device)

                output_images = self.model(guide_images, style_images)

                if save_path is not None:
                    save_images(output_images, save_path)