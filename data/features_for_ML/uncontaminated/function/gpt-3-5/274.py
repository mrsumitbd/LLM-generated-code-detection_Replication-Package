def _upload_partial_checkpoint_gr00t(hf_model_name: str, hf_token: str, output_dir: str = "/tmp/outputs/train") -> None:
    import os
    import requests

    checkpoints = [f for f in os.listdir(output_dir) if f.startswith("checkpoint-")]
    if not checkpoints:
        print("No checkpoints found to upload.")
        return

    latest_checkpoint = max(checkpoints)
    checkpoint_path = os.path.join(output_dir, latest_checkpoint)

    url = f"https://huggingface.co/{hf_model_name}/upload"
    headers = {"Authorization": f"Bearer {hf_token}"}
    files = {"file": open(checkpoint_path, "rb")}

    response = requests.post(url, headers=headers, files=files)
    if response.status_code != 200:
        print(f"Failed to upload checkpoint. Status code: {response.status_code}")
    else:
        print("Checkpoint uploaded successfully.")