import torch
import numpy as np
from typing import Tuple, Union, List

def generate_video_from_batch_with_loop(
    model: "ExtendDiffusionModel",
    state_shape: List[int],
    is_negative_prompt: bool,
    data_batch: dict,
    condition_latent: torch.Tensor,
    # hyper-parameters for inference
    num_of_loops: int,
    num_of_latent_overlap_list: List[int],
    guidance: float,
    num_steps: int,
    seed: int,
    add_input_frames_guidance: bool = False,
    augment_sigma_list: List[float] = None,
    data_batch_list: Union[None, List[dict]] = None,
    visualize: bool = False,
    save_fig_path: str = None,
    skip_reencode: int = 0,
    return_noise: bool = False,
    **extra_generate_kwargs,
) -> Tuple[np.ndarray, List[torch.Tensor], List[torch.Tensor], torch.Tensor] | Tuple[np.ndarray, List[torch.Tensor], List[torch.Tensor], torch.Tensor, torch.Tensor]:
    """
    Generate video with loop, given data batch. The condition latent will be updated at each loop.
    """
    # Validate inputs
    if num_of_loops < 1:
        raise ValueError("num_of_loops must be at least 1")
    if len(num_of_latent_overlap_list) != max(0, num_of_loops - 1):
        raise ValueError("num_of_latent_overlap_list length must be num_of_loops-1")
    if augment_sigma_list is not None and len(augment_sigma_list) != num_of_loops:
        raise ValueError("augment_sigma_list length must be num_of_loops")
    if data_batch_list is not None and len(data_batch_list) != num_of_loops:
        raise ValueError("data_batch_list length must be num_of_loops")

    # Prepare lists to store results
    condition_latents: List[torch.Tensor] = []
    sample_latents: List[torch.Tensor] = []
    noises: List[torch.Tensor] = []

    # Current condition latent (will be updated each loop)
    cur_condition_latent = condition_latent

    for i in range(num_of_loops):
        # Determine batch for this loop
        batch = data_batch_list[i] if data_batch_list is not None else data_batch

        # Set seed for reproducibility
        torch.manual_seed(seed + i)

        # Augment sigma for this loop
        sigma = augment_sigma_list[i] if augment_sigma_list is not None else None

        # Generate latent and noise for this loop
        # The exact signature of model.generate_video may vary; we pass common arguments
        # and rely on keyword matching.
        kwargs = {
            "batch": batch,
            "condition_latent": cur_condition_latent,
            "guidance": guidance,
            "num_steps": num_steps,
            "seed": seed + i,
            "add_input_frames_guidance": add_input_frames_guidance,
            "augment_sigma": sigma,
            "skip_reencode": skip_reencode,
            "is_negative_prompt": is_negative_prompt,
        }
        kwargs.update(extra_generate_kwargs)

        # Call the model's generate function
        # We expect it to return (latent, noise)
        latent, noise = model.generate_video(**kwargs)

        # Store results
        condition_latents.append(cur_condition_latent)
        sample_latents.append(latent)
        noises.append(noise)

        # Update condition latent for next loop
        cur_condition_latent = latent

    # Combine latents with overlap
    combined_latent = sample_latents[0]
    for idx in range(1, num_of_loops):
        overlap = num_of_latent_overlap_list[idx - 1]
        # Skip the overlapping frames from the new latent
        new_part = sample_latents[idx][:, overlap:, :, :, :]
        combined_latent = torch.cat([combined_latent, new_part], dim=1)

    # Decode the combined latent to video
    # Assume model.decode_latent returns shape (B, T, H, W, C)
    video = model.decode_latent(combined_latent, state_shape=state_shape)

    # Convert to numpy array in shape (T, H, W, C) with values in [0, 255]
    # Assume video is in [0,1] range
    video_np = video.squeeze(0).permute(1, 2, 3, 0).cpu().numpy()
    video_np = np.clip(video_np * 255.0, 0, 255).astype(np.uint8)

    # Visualize if requested
    if visualize:
        try:
            model.visualize_latent(combined_latent, save_fig_path=save_fig_path)
        except Exception:
            # If the model does not provide a visualization method, ignore
            pass

    # Return noise if requested
    if return_noise:
        # Return the noise from the last loop (shape BCTHW)
        return video_np, condition_latents, sample_latents, noises[-1]
    else:
        return video_np, condition_latents, sample_latents