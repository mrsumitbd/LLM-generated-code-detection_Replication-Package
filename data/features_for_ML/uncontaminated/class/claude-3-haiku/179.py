import numpy as np
from PIL import Image
import cv2

class DepthAnythingModel:

    def __init__(self):
        # Load the pre-trained depth estimation model here
        self.model = load_depth_model()

    def predict_depth(self, image: Image.Image) -> Image.Image:
        # Convert the input image to a numpy array
        image_np = np.array(image)

        # Pass the image through the depth estimation model
        depth_map = self.model.predict(image_np)

        # Convert the depth map to a PIL Image and return it
        depth_image = self.save_depth(depth_map)
        return depth_image

    def __call__(self, input_video: str, output_video: str = "depth.mp4") -> str:
        # Open the input video
        cap = cv2.VideoCapture(input_video)

        # Get the video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a video writer to save the depth frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        # Process each frame and write the depth map to the output video
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            depth_map = self.predict_depth(Image.fromarray(frame))
            out.write(np.array(depth_map))

        # Release the video capture and writer
        cap.release()
        out.release()

        return output_video

    @staticmethod
    def save_depth(output: np.ndarray) -> Image.Image:
        # Normalize the depth map to the range [0, 255]
        depth_image = (output - output.min()) / (output.max() - output.min())
        depth_image = (depth_image * 255).astype(np.uint8)

        # Convert the depth map to a PIL Image and return it
        return Image.fromarray(depth_image)

    @staticmethod
    def write_video(frames, output_path, fps=30):
        # Create a video writer to save the frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        height, width, _ = frames[0].shape
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Write the frames to the output video
        for frame in frames:
            out.write(frame)

        # Release the video writer
        out.release()