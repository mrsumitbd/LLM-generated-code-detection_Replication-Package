from cosmos_transfer1.utils import log
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union
import einops
import numpy as np
import os
import torch
from cosmos_transfer1.diffusion.training.models.extend_model import ExtendDiffusionModel

def generate_video_from_batch_with_loop(
    model: ExtendDiffusionModel,
    state_shape: list[int],
    is_negative_prompt: bool,
    data_batch: dict,
    condition_latent: torch.Tensor,
    # hyper-parameters for inference
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
    """Generate video with loop, given data batch. The condition latent will be updated at each loop.
    Args:
        model (ExtendDiffusionModel)
        state_shape (list): shape of the state tensor
        is_negative_prompt (bool): whether to use negative prompt

        data_batch (dict): data batch for video generation
        condition_latent (torch.Tensor): condition latent in shape BCTHW

        num_of_loops (int): number of loops to generate video
        num_of_latent_overlap_list (list[int]): list number of latent frames to overlap between clips, different clips can have different overlap
        guidance (float): The guidance scale to use during sample generation; defaults to 5.0.
        num_steps (int): number of steps for diffusion sampling
        seed (int): random seed for sampling
        add_input_frames_guidance (bool): whether to add image guidance, default is False
        augment_sigma_list (list): list of sigma value for the condition corruption at different clip, used when apply_corruption_to_condition_region is "noise_with_sigma" or "noise_with_sigma_fixed". default is None

        data_batch_list (list): list of data batch for video generation, used when num_of_loops >= 1, to support multiple prompts in auto-regressive generation. default is None
        visualize (bool): whether to visualize the latent and grid, default is False
        save_fig_path (str): path to save the visualization, default is None

        skip_reencode (int): whether to skip re-encode the input frames, default is 0
        return_noise (bool): whether to return the initial noise used for sampling, used for ODE pairs generation. Default is False
    Returns:
        np.array: generated video in shape THWC, range [0, 255]
        list: list of condition latent, each in shape BCTHW
        list: list of sample latent, each in shape BCTHW
        torch.Tensor: initial noise used for sampling, shape BCTHW (if return_noise is True)
    """
    if data_batch_list is None:
        data_batch_list = [data_batch for _ in range(num_of_loops)]
    if visualize:
        assert save_fig_path is not None, "save_fig_path should be set when visualize is True"

    # Generate video with loop
    condition_latent_list = []
    decode_latent_list = []  # list collect the latent token to be decoded at the end
    sample_latent = []
    grid_list = []

    augment_sigma_list = (
        model.config.conditioner.video_cond_bool.apply_corruption_to_condition_region_sigma_value
        if augment_sigma_list is None
        else augment_sigma_list
    )

    for i in range(num_of_loops):
        num_of_latent_overlap_i = num_of_latent_overlap_list[i]
        num_of_latent_overlap_i_plus_1 = (
            num_of_latent_overlap_list[i + 1]
            if i + 1 < len(num_of_latent_overlap_list)
            else num_of_latent_overlap_list[-1]
        )
        if condition_latent.shape[2] < state_shape[1]:
            # Padding condition latent to state shape
            log.info(f"Padding condition latent {condition_latent.shape} to state shape {state_shape}")
            b, c, t, h, w = condition_latent.shape
            condition_latent = torch.cat(
                [
                    condition_latent[:, :, :1],
                    condition_latent.new_zeros(b, c, state_shape[1] - t, h, w),
                    condition_latent[:, :, -1:],
                ],
                dim=2,
            ).contiguous()
            log.info(f"after padding, condition latent shape {condition_latent.shape}")
        log.info(f"Generate video loop {i} / {num_of_loops}")
        if visualize:
            log.info(f"Visualize condition latent {i}")
            visualize_latent_tensor_bcthw(
                condition_latent[:, :, :4].float(),
                nrow=4,
                save_fig_path=os.path.join(save_fig_path, f"loop_{i:02d}_condition_latent_first_4.png"),
            )  # BCTHW

        condition_latent_list.append(condition_latent)

        if i < len(augment_sigma_list):
            condition_video_augment_sigma_in_inference = augment_sigma_list[i]
            log.info(f"condition_video_augment_sigma_in_inference {condition_video_augment_sigma_in_inference}")
        else:
            condition_video_augment_sigma_in_inference = augment_sigma_list[-1]
        assert not add_input_frames_guidance, "add_input_frames_guidance should be False, not supported"
        sample = model.generate_samples_from_batch(
            data_batch_list[i],
            guidance=guidance,
            state_shape=state_shape,
            num_steps=num_steps,
            is_negative_prompt=is_negative_prompt,
            seed=seed + i,
            condition_latent=condition_latent,
            num_condition_t=num_of_latent_overlap_i,
            condition_video_augment_sigma_in_inference=condition_video_augment_sigma_in_inference,
            return_noise=return_noise,
            **extra_generate_kwargs,
        )

        if return_noise:
            sample, noise = sample

        if visualize:
            log.info(f"Visualize sampled latent {i} 4-8 frames")
            visualize_latent_tensor_bcthw(
                sample[:, :, 4:8].float(),
                nrow=4,
                save_fig_path=os.path.join(save_fig_path, f"loop_{i:02d}_sample_latent_last_4.png"),
            )  # BCTHW

            diff_between_sample_and_condition = (sample - condition_latent)[:, :, :num_of_latent_overlap_i]
            log.info(
                f"Visualize diff between sample and condition latent {i} first 4 frames {diff_between_sample_and_condition.mean()}"
            )

        sample_latent.append(sample)
        T = condition_latent.shape[2]
        assert num_of_latent_overlap_i <= T, f"num_of_latent_overlap should be < T, get {num_of_latent_overlap_i}, {T}"

        if model.config.conditioner.video_cond_bool.sample_tokens_start_from_p_or_i:
            assert skip_reencode, "skip_reencode should be turned on when sample_tokens_start_from_p_or_i is True"
            if i == 0:
                decode_latent_list.append(sample)
            else:
                decode_latent_list.append(sample[:, :, num_of_latent_overlap_i:])
        else:
            # Interpolator mode. Decode the first and last as an image.
            # each decode should operate on pixe_chunk_duration, otherwise the output will be incorrect.
            # Interpolator works on pixel_chunk_duration==1.
            # the root cause is the mean,std will be incorrect if decode a size different from pixel_chunk_duration.
            if model.config.conditioner.video_cond_bool.condition_location == "first_and_last_1":
                grid_BCTHW_list = []
                chunk_size = model.tokenizer.video_vae.pixel_chunk_duration
                for idx in range(sample.shape[2], chunk_size):
                    grid_BCTHW = (1.0 + model.decode(sample[:, :, idx : idx + chunk_size, ...])).clamp(
                        0, 2
                    ) / 2  # [B, 3, 1, H, W], [0, 1]
                    grid_BCTHW_list.append(grid_BCTHW)
                grid_BCTHW = torch.cat(grid_BCTHW_list, dim=2)  # [B, 3, T, H, W], [0, 1]
            else:
                grid_BCTHW = (1.0 + model.decode(sample)).clamp(0, 2) / 2  # [B, 3, T, H, W], [0, 1]

            if visualize:
                log.info(f"Visualize grid {i}")
                visualize_tensor_bcthw(
                    grid_BCTHW.float(), nrow=5, save_fig_path=os.path.join(save_fig_path, f"loop_{i:02d}_grid.png")
                )
            grid_np_THWC = (
                (grid_BCTHW[0].permute(1, 2, 3, 0) * 255).to(torch.uint8).cpu().numpy().astype(np.uint8)
            )  # THW3, range [0, 255]

            # Post-process the output: cut the conditional frames from the output if it's not the first loop
            num_cond_frames = compute_num_frames_condition(
                model, num_of_latent_overlap_i_plus_1, downsample_factor=model.tokenizer.temporal_compression_factor
            )
            if i == 0:
                new_grid_np_THWC = grid_np_THWC  # First output, dont cut the conditional frames
            else:
                new_grid_np_THWC = grid_np_THWC[
                    num_cond_frames:
                ]  # Remove the conditional frames from the output, since it's overlapped with previous loop
            grid_list.append(new_grid_np_THWC)

            # Prepare the next loop: re-compute the condition latent
            if hasattr(model, "n_cameras"):
                grid_BCTHW = einops.rearrange(grid_BCTHW, "B C (V T) H W -> (B V) C T H W", V=model.n_cameras)
            condition_frame_input = grid_BCTHW[:, :, -num_cond_frames:] * 2 - 1  # BCTHW, range [0, 1] to [-1, 1]
        if skip_reencode:
            # Use the last num_of_latent_overlap latent token as condition latent
            log.info(f"Skip re-encode the condition frames, use the last {num_of_latent_overlap_i_plus_1} latent token")
            condition_latent = sample[:, :, -num_of_latent_overlap_i_plus_1:]
        else:
            # Re-encode the condition frames to get the new condition latent
            condition_latent, _ = create_condition_latent_from_input_frames(
                model, condition_frame_input, num_frames_condition=num_cond_frames
            )  # BCTHW
        condition_latent = condition_latent.to(torch.bfloat16)

    # save videos
    if model.config.conditioner.video_cond_bool.sample_tokens_start_from_p_or_i:
        # decode all video together
        decode_latent_list = torch.cat(decode_latent_list, dim=2)
        grid_BCTHW = (1.0 + model.decode(decode_latent_list)).clamp(0, 2) / 2  # [B, 3, T, H, W], [0, 1]
        video_THWC = (
            (grid_BCTHW[0].permute(1, 2, 3, 0) * 255).to(torch.uint8).cpu().numpy().astype(np.uint8)
        )  # THW3, range [0, 255]
    else:
        video_THWC = np.concatenate(grid_list, axis=0)  # THW3, range [0, 255]

    if return_noise:
        return video_THWC, condition_latent_list, sample_latent, noise
    return video_THWC, condition_latent_list, sample_latent