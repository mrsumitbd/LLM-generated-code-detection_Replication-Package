def get_aksk():
    import os
    from pathlib import Path
    
    # Try to get from environment variables first
    ak = os.environ.get('HUGGING_FACE_HUB_TOKEN') or os.environ.get('HF_TOKEN')
    sk = os.environ.get('HF_SECRET_KEY')
    
    if ak and sk:
        return ak, sk
    
    # Try to read from huggingface config file
    hf_config_path = Path.home() / '.huggingface' / 'token'
    if hf_config_path.exists():
        ak = hf_config_path.read_text().strip()
        if ak:
            return ak, sk or ''
    
    # Try to read from credentials file
    cred_path = Path.home() / '.credentials'
    if cred_path.exists():
        try:
            import json
            creds = json.loads(cred_path.read_text())
            ak = creds.get('access_key')
            sk = creds.get('secret_key')
            if ak and sk:
                return ak, sk
        except:
            pass
    
    # Return environment variables or empty strings
    return ak or '', sk or ''