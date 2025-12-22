class FrameEnhancers:

    def __init__(self, models_processor: 'ModelsProcessor'):
        self.models_processor = models_processor

    def run_enhance_frame_tile_process(self, img, enhancer_type, tile_size=256, scale=1):
        """Process image enhancement with tiling to handle large images"""
        import numpy as np
        from PIL import Image
        
        if isinstance(img, Image.Image):
            img_array = np.array(img)
        else:
            img_array = img
            
        height, width = img_array.shape[:2]
        
        if height <= tile_size and width <= tile_size:
            return self._apply_enhancer(img_array, enhancer_type)
        
        # Process with tiling
        tiles = []
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                y_end = min(y + tile_size, height)
                x_end = min(x + tile_size, width)
                tile = img_array[y:y_end, x:x_end]
                enhanced_tile = self._apply_enhancer(tile, enhancer_type)
                tiles.append((y, x, enhanced_tile))
        
        # Reconstruct image from tiles
        if scale > 1:
            new_height = height * scale
            new_width = width * scale
        else:
            new_height = height
            new_width = width
            
        result = np.zeros((new_height, new_width, img_array.shape[2] if len(img_array.shape) > 2 else 1), dtype=img_array.dtype)
        
        for y, x, tile in tiles:
            if scale > 1:
                y_start = y * scale
                x_start = x * scale
                y_end = y_start + tile.shape[0]
                x_end = x_start + tile.shape[1]
            else:
                y_start = y
                x_start = x
                y_end = y_start + tile.shape[0]
                x_end = x_start + tile.shape[1]
            result[y_start:y_end, x_start:x_end] = tile
        
        return result

    def _apply_enhancer(self, img, enhancer_type):
        """Apply the specified enhancer to an image"""
        enhancer_map = {
            'realesrganx2': self.run_realesrganx2,
            'realesrganx4': self.run_realesrganx4,
            'realesrx4v3': self.run_realesrx4v3,
            'bsrganx2': self.run_bsrganx2,
            'bsrganx4': self.run_bsrganx4,
            'ultrasharpx4': self.run_ultrasharpx4,
            'ultramixx4': self.run_ultramixx4,
            'deoldify_artistic': self.run_deoldify_artistic,
            'deoldify_stable': self.run_deoldify_stable,
            'deoldify_video': self.run_deoldify_video,
            'ddcolor_artistic': self.run_ddcolor_artistic,
            'ddcolor': self.run_ddcolor,
        }
        
        if enhancer_type in enhancer_map:
            return enhancer_map[enhancer_type](img, None)
        return img

    def run_realesrganx2(self, image, output):
        model = self.models_processor.get_model('realesrganx2')
        return model.enhance(image)

    def run_realesrganx4(self, image, output):
        model = self.models_processor.get_model('realesrganx4')
        return model.enhance(image)

    def run_realesrx4v3(self, image, output):
        model = self.models_processor.get_model('realesrx4v3')
        return model.enhance(image)

    def run_bsrganx2(self, image, output):
        model = self.models_processor.get_model('bsrganx2')
        return model.enhance(image)

    def run_bsrganx4(self, image, output):
        model = self.models_processor.get_model('bsrganx4')
        return model.enhance(image)

    def run_ultrasharpx4(self, image, output):
        model = self.models_processor.get_model('ultrasharpx4')
        return model.enhance(image)

    def run_ultramixx4(self, image, output):
        model = self.models_processor.get_model('ultramixx4')
        return model.enhance(image)

    def run_deoldify_artistic(self, image, output):
        model = self.models_processor.get_model('deoldify_artistic')
        return model.colorize(image)

    def run_deoldify_stable(self, image, output):
        model = self.models_processor.get_model('deoldify_stable')
        return model.colorize(image)

    def run_deoldify_video(self, image, output):
        model = self.models_processor.get_model('deoldify_video')
        return model.colorize(image)

    def run_ddcolor_artistic(self, image, output):
        model = self.models_processor.get_model('ddcolor_artistic')
        return model.colorize(image)

    def run_ddcolor(self, image, output):
        model = self.models_processor.get_model('ddcolor')
        return model.colorize(image)