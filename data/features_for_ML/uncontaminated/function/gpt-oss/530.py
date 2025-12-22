import torch

# Global dictionary to keep track of readiness events per (rank, segment)
_ready_events = {}

def set_ready(rank, segment, stream: torch.cuda.Stream):
    """
    Mark the given segment on the specified rank as ready by recording a CUDA event
    on the provided stream. The event can later be used to synchronize or check
    readiness status.
    """
    # Create a non-blocking CUDA event
    event = torch.cuda.Event(blocking=False)
    # Record the event on the given stream
    event.record(stream)
    # Store the event in the global dictionary keyed by (rank, segment)
    _ready_events[(rank, segment)] = event