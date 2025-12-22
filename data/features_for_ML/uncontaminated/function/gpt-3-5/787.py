from typing import Tuple, Union
import torch
import numpy as np

def generate_video_from_batch_with_loop(
    model,
    state_shape,
    is_negative_prompt,
    data_batch,
    condition_latent,
    num_of_loops,
    num_of_latent_overlap_list,
    guidance,
    num_steps,
    seed,
    add_input_frames_guidance=False,
    augment_sigma_list=None,
    data_batch_list=None,
    visualize=False,
    save_fig_path=None,
    skip_reencode=0,
    return_noise=False,
    **extra_generate_kwargs,
) -> Union[Tuple[np.array, list, list, torch.Tensor], Tuple[np.array, list, list, torch.Tensor, torch.Tensor]]:
    pass