def set_ready(rank, segment, stream: torch.cuda.Stream):
    with torch.cuda.stream(stream):
        torch.cuda.current_stream().wait_stream(stream)
        torch.cuda.synchronize()
        torch.cuda.current_stream().record_event()