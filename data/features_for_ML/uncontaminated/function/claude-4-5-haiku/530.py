def set_ready(rank, segment, stream: torch.cuda.Stream):
    """Set a segment as ready for a given rank using CUDA events."""
    if not hasattr(set_ready, '_events'):
        set_ready._events = {}
    
    key = (rank, segment)
    
    if key not in set_ready._events:
        set_ready._events[key] = torch.cuda.Event()
    
    set_ready._events[key].record(stream)