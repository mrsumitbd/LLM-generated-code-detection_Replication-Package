import numpy as np
from PIL import Image
from typing import Tuple
from .models_processor import ModelsProcessor

class FrameEnhancers:
    def __init__(self, models_processor: 'ModelsProcessor'):
        self.models_processor = models_processor

    def run_enhance_frame_tile_process(self, img, enhancer_type, tile_size=256, scale=1):
        height, width = img.shape[:2]
        tiles = self._create_tiles(img, tile_size)
        enhanced_tiles = []

        for tile in tiles:
            enhanced_tile = self._run_enhancer(tile, enhancer_type)
            enhanced_tiles.append(enhanced_tile)

        enhanced_img = self._stitch_tiles(enhanced_tiles, height, width, tile_size, scale)
        return enhanced_img

    def run_realesrganx2(self, image, output):
        enhanced_image = self._run_enhancer(image, 'realesrganx2')
        Image.fromarray(enhanced_image).save(output)

    def run_realesrganx4(self, image, output):
        enhanced_image = self._run_enhancer(image, 'realesrganx4')
        Image.fromarray(enhanced_image).save(output)

    def run_realesrx4v3(self, image, output):
        enhanced_image = self._run_enhancer(image, 'realesrx4v3')
        Image.fromarray(enhanced_image).save(output)

    def run_bsrganx2(self, image, output):
        enhanced_image = self._run_enhancer(image, 'bsrganx2')
        Image.fromarray(enhanced_image).save(output)

    def run_bsrganx4(self, image, output):
        enhanced_image = self._run_enhancer(image, 'bsrganx4')
        Image.fromarray(enhanced_image).save(output)

    def run_ultrasharpx4(self, image, output):
        enhanced_image = self._run_enhancer(image, 'ultrasharpx4')
        Image.fromarray(enhanced_image).save(output)

    def run_ultramixx4(self, image, output):
        enhanced_image = self._run_enhancer(image, 'ultramixx4')
        Image.fromarray(enhanced_image).save(output)

    def run_deoldify_artistic(self, image, output):
        enhanced_image = self._run_enhancer(image, 'deoldify_artistic')
        Image.fromarray(enhanced_image).save(output)

    def run_deoldify_stable(self, image, output):
        enhanced_image = self._run_enhancer(image, 'deoldify_stable')
        Image.fromarray(enhanced_image).save(output)

    def run_deoldify_video(self, image, output):
        enhanced_image = self._run_enhancer(image, 'deoldify_video')
        Image.fromarray(enhanced_image).save(output)

    def run_ddcolor_artistic(self, image, output):
        enhanced_image = self._run_enhancer(image, 'ddcolor_artistic')
        Image.fromarray(enhanced_image).save(output)

    def run_ddcolor(self, image, output):
        enhanced_image = self._run_enhancer(image, 'ddcolor')
        Image.fromarray(enhanced_image).save(output)

    def _run_enhancer(self, image, enhancer_type):
        enhancer = getattr(self.models_processor, f'run_{enhancer_type}')
        return enhancer(image)

    def _create_tiles(self, img, tile_size) -> Tuple[np.ndarray]:
        height, width = img.shape[:2]
        tiles = []
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tile = img[y:y+tile_size, x:x+tile_size]
                tiles.append(tile)
        return tiles

    def _stitch_tiles(self, tiles, height, width, tile_size, scale):
        enhanced_img = np.zeros((height, width, 3), dtype=np.uint8)
        tile_idx = 0
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tile = tiles[tile_idx]
                if scale != 1:
                    tile = self._resize_image(tile, scale)
                enhanced_img[y:y+tile.shape[0], x:x+tile.shape[1]] = tile
                tile_idx += 1
        return enhanced_img

    def _resize_image(self, image, scale):
        new_size = (int(image.shape[1] * scale), int(image.shape[0] * scale))
        return np.array(Image.fromarray(image).resize(new_size, resample=Image.BICUBIC))