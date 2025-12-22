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
    
    device = condition_latent.device
    dtype = condition_latent.dtype
    
    condition_latent_list = []
    sample_latent_list = []
    all_noise = None
    
    current_condition_latent = condition_latent
    
    for loop_idx in range(num_of_loops):
        # Select data batch for this loop
        if data_batch_list is not None:
            current_data_batch = data_batch_list[loop_idx]
        else:
            current_data_batch = data_batch
        
        # Get augment sigma for this loop
        current_augment_sigma = None
        if augment_sigma_list is not None:
            current_augment_sigma = augment_sigma_list[loop_idx]
        
        # Get overlap for this loop
        current_overlap = num_of_latent_overlap_list[loop_idx] if isinstance(num_of_latent_overlap_list, list) else num_of_latent_overlap_list
        
        # Generate video for this loop
        sample_latent, noise = model.generate_video_from_batch(
            state_shape=state_shape,
            is_negative_prompt=is_negative_prompt,
            data_batch=current_data_batch,
            condition_latent=current_condition_latent,
            guidance=guidance,
            num_steps=num_steps,
            seed=seed + loop_idx,
            add_input_frames_guidance=add_input_frames_guidance,
            augment_sigma=current_augment_sigma,
            visualize=visualize,
            save_fig_path=save_fig_path,
            return_noise=True,
            **extra_generate_kwargs,
        )
        
        condition_latent_list.append(current_condition_latent.clone())
        sample_latent_list.append(sample_latent.clone())
        
        if return_noise:
            if all_noise is None:
                all_noise = noise.clone()
            else:
                all_noise = torch.cat([all_noise, noise], dim=2)
        
        # Update condition latent for next loop
        if loop_idx < num_of_loops - 1:
            # Extract the non-overlapping part from the generated sample
            if current_overlap > 0:
                # Keep the last 'overlap' frames from sample_latent as condition
                # and concatenate with the rest of the sample
                overlap_condition = sample_latent[:, :, -current_overlap:, :, :]
                current_condition_latent = overlap_condition
            else:
                # No overlap, use the entire sample as condition
                current_condition_latent = sample_latent
    
    # Decode all sample latents to video
    video_frames = []
    for sample_latent in sample_latent_list:
        frames = model.decode_latent_to_video(sample_latent)
        video_frames.append(frames)
    
    # Concatenate frames, removing overlaps
    final_frames = []
    for loop_idx, frames in enumerate(video_frames):
        if loop_idx == 0:
            final_frames.append(frames)
        else:
            overlap = num_of_latent_overlap_list[loop_idx] if isinstance(num_of_latent_overlap_list, list) else num_of_latent_overlap_list
            # Skip the first 'overlap' frames to avoid duplication
            if overlap > 0:
                final_frames.append(frames[overlap:])
            else:
                final_frames.append(frames)
    
    final_video = np.concatenate(final_frames, axis=0)
    
    if return_noise:
        return final_video, condition_latent_list, sample_latent_list, all_noise
    else:
        return final_video, condition_latent_list, sample_latent_list, None