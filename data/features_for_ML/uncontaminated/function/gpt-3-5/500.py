def batch(data, batch_type='static', batch_size=16, max_frames_in_batch=12000, mode='train'):
    if batch_type == 'static':
        return static_batch(data, batch_size, mode)
    elif batch_type == 'dynamic':
        return dynamic_batch(data, max_frames_in_batch, mode)
    else:
        raise ValueError("Invalid batch_type. Choose either 'static' or 'dynamic'.")

def static_batch(data, batch_size, mode):
    # Implement static batch logic here
    pass

def dynamic_batch(data, max_frames_in_batch, mode):
    # Implement dynamic batch logic here
    pass