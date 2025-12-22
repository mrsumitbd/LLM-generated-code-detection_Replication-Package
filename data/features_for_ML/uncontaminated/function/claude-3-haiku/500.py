def batch(data, batch_type='static', batch_size=16, max_frames_in_batch=12000, mode='train'):
    """ Wrapper for static/dynamic batch
    """
    if batch_type == 'static':
        return _static_batch(data, batch_size, max_frames_in_batch, mode)
    elif batch_type == 'dynamic':
        return _dynamic_batch(data, batch_size, max_frames_in_batch, mode)
    else:
        raise ValueError(f"Invalid batch_type: {batch_type}")

def _static_batch(data, batch_size, max_frames_in_batch, mode):
    batches = []
    for i in range(0, len(data), batch_size):
        batch_data = data[i:i+batch_size]
        if sum(len(item) for item in batch_data) <= max_frames_in_batch:
            batches.append(batch_data)
    return batches

def _dynamic_batch(data, batch_size, max_frames_in_batch, mode):
    batches = []
    current_batch = []
    current_batch_size = 0
    current_batch_frames = 0
    for item in data:
        item_frames = len(item)
        if current_batch_frames + item_frames <= max_frames_in_batch and len(current_batch) < batch_size:
            current_batch.append(item)
            current_batch_size += 1
            current_batch_frames += item_frames
        else:
            batches.append(current_batch)
            current_batch = [item]
            current_batch_size = 1
            current_batch_frames = item_frames
    if current_batch:
        batches.append(current_batch)
    return batches