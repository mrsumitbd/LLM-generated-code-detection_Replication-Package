import torch
import numpy as np
from typing import Tuple, Union

def generate_video_from_batch_with_loop(
    model: ExtendDiffusionModel,
    state_shape: list[int],
    is_negative_prompt: bool,
    data_batch: dict,
    condition_latent: torch.Tensor,
    num_of_loops: int,
    num_of_latent_overlap_list: list[int],
    guidance: float,
    num_steps: int,
    seed: int,
    add_input_frames_guidance: bool = False,
    augment_sigma_list: list[float] = None,
    data_batch_list: Union[None, list[dict]] = None,
    visualize: bool = False,
    save_fig_path: str = None,
    skip_reencode: int = 0,
    return_noise: bool = False,
    **extra_generate_kwargs,
) -> Tuple[np.array, list, list, torch.Tensor] | Tuple[np.array, list, list, torch.Tensor, torch.Tensor]:
    
    # Initialize the video, condition latent, and sample latent lists
    video = []
    condition_latents = []
    sample_latents = []
    
    # Set the random seed
    torch.manual_seed(seed)
    
    # Generate the video with loops
    for loop_idx in range(num_of_loops):
        # Get the current data batch
        if data_batch_list is not None:
            data_batch = data_batch_list[loop_idx]
        
        # Generate the video frames
        video_frames, sample_latent, condition_latent = model.generate_video_from_batch(
            data_batch=data_batch,
            condition_latent=condition_latent,
            num_of_latent_overlap=num_of_latent_overlap_list[loop_idx],
            guidance=guidance,
            num_steps=num_steps,
            add_input_frames_guidance=add_input_frames_guidance,
            augment_sigma=augment_sigma_list[loop_idx] if augment_sigma_list else None,
            skip_reencode=skip_reencode,
            **extra_generate_kwargs,
        )
        
        # Append the generated frames, condition latent, and sample latent to the lists
        video.append(video_frames)
        condition_latents.append(condition_latent)
        sample_latents.append(sample_latent)
        
        # Visualize the latent and grid if requested
        if visualize:
            model.visualize_latent_and_grid(
                condition_latent=condition_latent,
                sample_latent=sample_latent,
                save_fig_path=save_fig_path,
            )
    
    # Concatenate the video frames
    video = np.concatenate(video, axis=0)
    
    # Return the generated video, condition latents, sample latents, and optionally the initial noise
    if return_noise:
        return video, condition_latents, sample_latents, sample_latent[:1]
    else:
        return video, condition_latents, sample_latents