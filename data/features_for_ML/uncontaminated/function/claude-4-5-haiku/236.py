def get_modal_prefix():
    import os
    return os.environ.get('MODAL_PREFIX', '')