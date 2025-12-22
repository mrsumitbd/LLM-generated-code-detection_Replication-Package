def _upload_partial_checkpoint_gr00t(
    hf_model_name: str,
    hf_token: str,
    output_dir: str = "/tmp/outputs/train",
) -> None:
    """
    Uploads the latest checkpoint from a timed-out Gr00t training run
    to the Hugging Face Hub model repo. Fails safely if no checkpoints
    are found or an upload error occurs.
    """
    import os
    from pathlib import Path
    from huggingface_hub import HfApi, login
    
    try:
        # Authenticate with Hugging Face
        login(token=hf_token)
        
        # Check if output directory exists
        if not os.path.exists(output_dir):
            print(f"Output directory {output_dir} does not exist. No checkpoints to upload.")
            return
        
        # Find all checkpoint directories
        checkpoint_dirs = []
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path) and item.startswith("checkpoint-"):
                checkpoint_dirs.append((item, item_path))
        
        if not checkpoint_dirs:
            print(f"No checkpoints found in {output_dir}.")
            return
        
        # Sort by checkpoint number and get the latest
        checkpoint_dirs.sort(key=lambda x: int(x[0].split("-")[1]))
        latest_checkpoint_name, latest_checkpoint_path = checkpoint_dirs[-1]
        
        print(f"Found latest checkpoint: {latest_checkpoint_name}")
        
        # Initialize API and upload
        api = HfApi()
        
        # Upload the checkpoint directory
        api.upload_folder(
            folder_path=latest_checkpoint_path,
            repo_id=hf_model_name,
            token=hf_token,
            repo_type="model",
            commit_message=f"Upload partial checkpoint from timed-out training run: {latest_checkpoint_name}",
        )
        
        print(f"Successfully uploaded {latest_checkpoint_name} to {hf_model_name}")
        
    except Exception as e:
        print(f"Failed to upload checkpoint: {str(e)}")
        return