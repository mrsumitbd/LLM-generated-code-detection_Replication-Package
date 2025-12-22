class FrameEnhancers:

    def __init__(self, models_processor: 'ModelsProcessor'):
        self.models_processor = models_processor

    def run_enhance_frame_tile_process(self, img, enhancer_type, tile_size=256, scale=1):
        if enhancer_type == 'realesrganx2':
            return self.run_realesrganx2(img, output)
        elif enhancer_type == 'realesrganx4':
            return self.run_realesrganx4(img, output)
        elif enhancer_type == 'realesrx4v3':
            return self.run_realesrx4v3(img, output)
        elif enhancer_type == 'bsrganx2':
            return self.run_bsrganx2(img, output)
        elif enhancer_type == 'bsrganx4':
            return self.run_bsrganx4(img, output)
        elif enhancer_type == 'ultrasharpx4':
            return self.run_ultrasharpx4(img, output)
        elif enhancer_type == 'ultramixx4':
            return self.run_ultramixx4(img, output)
        elif enhancer_type == 'deoldify_artistic':
            return self.run_deoldify_artistic(img, output)
        elif enhancer_type == 'deoldify_stable':
            return self.run_deoldify_stable(img, output)
        elif enhancer_type == 'deoldify_video':
            return self.run_deoldify_video(img, output)
        elif enhancer_type == 'ddcolor_artistic':
            return self.run_ddcolor_artistic(img, output)
        elif enhancer_type == 'ddcolor':
            return self.run_ddcolor(img, output)
        else:
            raise ValueError(f"Unknown enhancer type: {enhancer_type}")

    def run_realesrganx2(self, image, output):
        # Implementation for realesrganx2
        pass

    def run_realesrganx4(self, image, output):
        # Implementation for realesrganx4
        pass

    def run_realesrx4v3(self, image, output):
        # Implementation for realesrx4v3
        pass

    def run_bsrganx2(self, image, output):
        # Implementation for bsrganx2
        pass

    def run_bsrganx4(self, image, output):
        # Implementation for bsrganx4
        pass

    def run_ultrasharpx4(self, image, output):
        # Implementation for ultrasharpx4
        pass

    def run_ultramixx4(self, image, output):
        # Implementation for ultramixx4
        pass

    def run_deoldify_artistic(self, image, output):
        # Implementation for deoldify_artistic
        pass

    def run_deoldify_stable(self, image, output):
        # Implementation for deoldify_stable
        pass

    def run_deoldify_video(self, image, output):
        # Implementation for deoldify_video
        pass

    def run_ddcolor_artistic(self, image, output):
        # Implementation for ddcolor_artistic
        pass

    def run_ddcolor(self, image, output):
        # Implementation for ddcolor
        pass