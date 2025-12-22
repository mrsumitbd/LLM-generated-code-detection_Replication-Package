def collate_fn(examples):
    """
    Collate function for batching examples in a DataLoader.
    Handles variable-length sequences and prepares them for model input.
    """
    import torch
    from torch.nn.utils.rnn import pad_sequence
    
    if not examples:
        return {}
    
    # Separate different fields from examples
    batch = {}
    
    # Get all keys from the first example
    keys = examples[0].keys() if isinstance(examples[0], dict) else None
    
    if keys is None:
        return examples
    
    for key in keys:
        values = [example[key] for example in examples]
        
        # Handle different data types
        if isinstance(values[0], torch.Tensor):
            # For tensors, pad sequences if they have different lengths
            if len(values[0].shape) > 0 and values[0].shape[0] != values[-1].shape[0]:
                batch[key] = pad_sequence(values, batch_first=True, padding_value=0)
            else:
                batch[key] = torch.stack(values)
        elif isinstance(values[0], (int, float)):
            # Convert numbers to tensor
            batch[key] = torch.tensor(values)
        elif isinstance(values[0], str):
            # Keep strings as list
            batch[key] = values
        elif isinstance(values[0], list):
            # Handle lists - try to convert to tensor if possible
            try:
                batch[key] = torch.tensor(values)
            except (ValueError, TypeError):
                batch[key] = values
        else:
            batch[key] = values
    
    return batch