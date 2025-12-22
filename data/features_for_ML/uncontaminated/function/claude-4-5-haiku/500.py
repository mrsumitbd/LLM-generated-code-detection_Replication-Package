def batch(data, batch_type='static', batch_size=16, max_frames_in_batch=12000, mode='train'):
    """ Wrapper for static/dynamic batch
    """
    if batch_type == 'static':
        return static_batch(data, batch_size, mode)
    elif batch_type == 'dynamic':
        return dynamic_batch(data, max_frames_in_batch, mode)
    else:
        raise ValueError(f"Unknown batch_type: {batch_type}")


def static_batch(data, batch_size, mode):
    """Create batches of fixed size"""
    batches = []
    for i in range(0, len(data), batch_size):
        batch_data = data[i:i + batch_size]
        batches.append(batch_data)
    return batches


def dynamic_batch(data, max_frames_in_batch, mode):
    """Create batches based on maximum frames constraint"""
    batches = []
    current_batch = []
    current_frames = 0
    
    for sample in data:
        # Assume each sample has a 'frames' attribute or we calculate frames from shape
        if isinstance(sample, dict) and 'frames' in sample:
            sample_frames = sample['frames']
        elif hasattr(sample, 'shape'):
            # Assume first dimension is frames
            sample_frames = sample.shape[0]
        else:
            sample_frames = len(sample)
        
        # If adding this sample exceeds max frames and batch is not empty, start new batch
        if current_frames + sample_frames > max_frames_in_batch and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_frames = 0
        
        current_batch.append(sample)
        current_frames += sample_frames
    
    # Add remaining batch
    if current_batch:
        batches.append(current_batch)
    
    return batches