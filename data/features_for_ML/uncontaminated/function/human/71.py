import torch
from PIL import Image

def fetch_video(
    ele: dict, return_video_sample_fps: bool = False
) -> torch.Tensor | list[Image.Image]:
    if isinstance(ele['video'], str):
        video_reader_backend = get_video_reader_backend()
        try:
            video, sample_fps, timestamps = VIDEO_READER_BACKENDS[video_reader_backend](ele)
        except Exception as e:
            logger.warning(
                f'video_reader_backend {video_reader_backend} error, use torchvision as default, msg: {e}'
            )
            video, sample_fps, timestamps = VIDEO_READER_BACKENDS['torchvision'](ele)

        nframes, _, height, width = video.shape

        if return_video_sample_fps:
            return video, sample_fps, timestamps
        return video
    else:
        assert isinstance(ele['video'], (list, tuple))
        process_info = ele.copy()
        process_info.pop('type', None)
        process_info.pop('video', None)
        images = [
            fetch_image({'image': video_element, **process_info}) for video_element in ele['video']
        ]
        nframes = adjust_by_factor(len(images), FRAME_FACTOR, method='ceil')
        if len(images) < nframes:
            images.extend([images[-1]] * (nframes - len(images)))

        timestamps = [-1 for i in range(nframes)]  # not sure about this
        if return_video_sample_fps:
            return images, process_info.pop('fps', 2.0), timestamps
        return images