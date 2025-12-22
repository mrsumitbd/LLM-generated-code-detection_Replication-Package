class FrameEnhancers:
    """
    Wrapper around a ModelsProcessor instance that exposes a convenient API for
    running various image enhancement models.
    """

    def __init__(self, models_processor: 'ModelsProcessor'):
        """
        Store the provided ModelsProcessor instance for later use.

        Parameters
        ----------
        models_processor : ModelsProcessor
            An object that implements the actual model inference logic.
        """
        self.models_processor = models_processor

    # ------------------------------------------------------------------
    # Generic tile‑based enhancement
    # ------------------------------------------------------------------
    def run_enhance_frame_tile_process(self, img, enhancer_type, tile_size=256, scale=1):
        """
        Run a tile‑based enhancement on the given image.

        Parameters
        ----------
        img : numpy.ndarray or PIL.Image
            The input image.
        enhancer_type : str
            Identifier of the enhancer to use.
        tile_size : int, optional
            Size of the tiles to split the image into.
        scale : int, optional
            Upscaling factor.

        Returns
        -------
        numpy.ndarray
            The enhanced image.
        """
        # Delegate to the underlying processor
        return self.models_processor.enhance_frame_tile_process(
            img, enhancer_type, tile_size=tile_size, scale=scale
        )

    # ------------------------------------------------------------------
    # Real-ESRGAN
    # ------------------------------------------------------------------
    def run_realesrganx2(self, image, output):
        return self.models_processor.realesrgan_x2(image, output)

    def run_realesrganx4(self, image, output):
        return self.models_processor.realesrgan_x4(image, output)

    def run_realesrx4v3(self, image, output):
        return self.models_processor.realesr_x4_v3(image, output)

    # ------------------------------------------------------------------
    # BSRGAN
    # ------------------------------------------------------------------
    def run_bsrganx2(self, image, output):
        return self.models_processor.bsrgan_x2(image, output)

    def run_bsrganx4(self, image, output):
        return self.models_processor.bsrgan_x4(image, output)

    # ------------------------------------------------------------------
    # UltraSharp
    # ------------------------------------------------------------------
    def run_ultrasharpx4(self, image, output):
        return self.models_processor.ultrasharp_x4(image, output)

    # ------------------------------------------------------------------
    # UltraMix
    # ------------------------------------------------------------------
    def run_ultramixx4(self, image, output):
        return self.models_processor.ultramix_x4(image, output)

    # ------------------------------------------------------------------
    # DeOldify
    # ------------------------------------------------------------------
    def run_deoldify_artistic(self, image, output):
        return self.models_processor.deoldify_artistic(image, output)

    def run_deoldify_stable(self, image, output):
        return self.models_processor.deoldify_stable(image, output)

    def run_deoldify_video(self, image, output):
        return self.models_processor.deoldify_video(image, output)

    # ------------------------------------------------------------------
    # DDColor
    # ------------------------------------------------------------------
    def run_ddcolor_artistic(self, image, output):
        return self.models_processor.ddcolor_artistic(image, output)

    def run_ddcolor(self, image, output):
        return self.models_processor.ddcolor(image, output)