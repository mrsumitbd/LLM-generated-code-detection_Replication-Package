import grpc

def SendStreamingMessage(request,
                         target,
                         options=(),
                         channel_credentials=None,
                         call_credentials=None,
                         insecure=False,
                         compression=None,
                         wait_for_ready=None,
                         timeout=None,
                         metadata=None):
    with grpc.secure_channel(target, channel_credentials) if channel_credentials else grpc.insecure_channel(target) as channel:
        with grpc.call_options(options=options,
                              credentials=call_credentials,
                              compression=compression,
                              wait_for_ready=wait_for_ready,
                              timeout=timeout,
                              metadata=metadata) as call_options:
            stub = channel.unary_stream(request, **call_options)
            for response in stub:
                yield response