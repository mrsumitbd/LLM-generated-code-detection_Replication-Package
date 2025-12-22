import torch

def set_ready(rank, segment, stream: torch.cuda.Stream):
    with torch.cuda.stream(stream):
        torch.cuda.synchronize(device=rank)
        segment.record_stream(stream)