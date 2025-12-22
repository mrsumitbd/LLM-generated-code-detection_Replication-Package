def save_image_or_video_multiview(
    tensor: Tensor, save_path: str | IO[Any], fps: int = 24, quality=None, ffmpeg_params=None, n_views: int = 1
) -> None:
    """
    Split the tensor into n_views, stack them along the width dimension, and save as a video
        Args:
        tensor (Tensor): Input tensor with shape (B, C, T, H, W) or (C, T, H, W) in [-1, 1] or [0, 1] range.
            If in [-1, 1] range, it will be automatically converted to [0, 1] range.
        save_path (Union[str, IO[Any]]): File path (with or without extension) or file-like object.
        fps (int): Frames per second for video. Default is 24.
        quality: Optional quality parameter for images (passed to easy_io).
        ffmpeg_params: Optional ffmpeg parameters for videos (passed to easy_io).
    """
    import torch
    from torchvision.io import write_video
    from torchvision.transforms.functional import to_pil_image
    import numpy as np
    
    # Handle batch dimension
    if tensor.ndim == 5:  # (B, C, T, H, W)
        tensor = tensor[0]  # Take first batch
    
    # tensor shape: (C, T, H, W)
    C, T, H, W = tensor.shape
    
    # Convert from [-1, 1] to [0, 1] if needed
    if tensor.min() < 0:
        tensor = (tensor + 1) / 2
    
    # Ensure tensor is in [0, 1] range
    tensor = torch.clamp(tensor, 0, 1)
    
    # Split into n_views along the channel dimension
    view_tensors = torch.split(tensor, C // n_views, dim=0)
    
    # Process each view: (C_per_view, T, H, W) -> (T, H, W*n_views, 3)
    frames_list = []
    
    for t in range(T):
        frame_views = []
        for view_idx in range(n_views):
            view_tensor = view_tensors[view_idx][:, t, :, :]  # (C_per_view, H, W)
            
            # Convert to RGB if needed
            if view_tensor.shape[0] == 1:
                view_tensor = view_tensor.repeat(3, 1, 1)
            elif view_tensor.shape[0] == 4:
                view_tensor = view_tensor[:3]
            
            # Ensure it's 3 channels
            if view_tensor.shape[0] != 3:
                view_tensor = view_tensor[:3]
            
            frame_views.append(view_tensor)
        
        # Stack views horizontally (along width)
        combined_frame = torch.cat(frame_views, dim=2)  # (3, H, W*n_views)
        frames_list.append(combined_frame)
    
    # Stack all frames: (T, 3, H, W*n_views)
    video_tensor = torch.stack(frames_list, dim=0)
    
    # Convert to uint8 format for video writing
    video_tensor = (video_tensor * 255).to(torch.uint8)
    
    # Determine if saving as video or image
    if isinstance(save_path, str):
        if T == 1:
            # Single frame - save as image
            frame = video_tensor[0].permute(1, 2, 0).cpu().numpy()
            from PIL import Image
            img = Image.fromarray(frame)
            img.save(save_path)
        else:
            # Multiple frames - save as video
            write_video(save_path, video_tensor, fps=fps)
    else:
        # File-like object
        if T == 1:
            frame = video_tensor[0].permute(1, 2, 0).cpu().numpy()
            from PIL import Image
            img = Image.fromarray(frame)
            img.save(save_path)
        else:
            write_video(save_path, video_tensor, fps=fps)