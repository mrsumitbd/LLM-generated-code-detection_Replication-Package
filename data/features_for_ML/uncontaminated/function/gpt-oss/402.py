import grpc
from grpc.experimental import dynamic_stub

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
    """
    Send a streaming message using gRPC.

    Parameters
    ----------
    request : protobuf message
        The request message to send.  The descriptor of the message
        must contain the full RPC method name in the form
        ``package.Service.Method``.
    target : str
        The target address of the server (e.g. ``localhost:50051``).
    options : tuple, optional
        Channel options.
    channel_credentials : grpc.ChannelCredentials, optional
        Credentials for a secure channel.
    call_credentials : grpc.CallCredentials, optional
        Call‑level credentials.
    insecure : bool, optional
        If True, create an insecure channel.
    compression : grpc.Compression, optional
        Compression to use for the channel.
    wait_for_ready : bool, optional
        Whether to wait for the channel to become ready.
    timeout : float, optional
        Timeout for the RPC call.
    metadata : list of tuples, optional
        Metadata to send with the RPC.

    Returns
    -------
    Any
        The result of the RPC call.  For streaming RPCs this will be an
        iterator over the response messages.
    """
    # Create the channel
    if insecure:
        channel = grpc.insecure_channel(target, options=options, compression=compression)
    else:
        channel = grpc.secure_channel(target,
                                      channel_credentials,
                                      options=options,
                                      compression=compression)

    # Attach call‑level credentials if provided
    if call_credentials:
        # grpc.composite_call_credentials requires a channel credential; if none,
        # we simply use the call credentials directly.
        if channel_credentials:
            channel = grpc.intercept_channel(
                channel,
                grpc.composite_call_credentials(channel_credentials, call_credentials)
            )
        else:
            channel = grpc.intercept_channel(channel, call_credentials)

    # Create a dynamic stub for the channel
    stub = dynamic_stub.DynamicStub(channel)

    # Determine the RPC method name from the request descriptor
    full_name = request.DESCRIPTOR.full_name  # e.g. "mypkg.MyService.MyMethod"
    method_name = full_name.split('.')[-1]

    # Retrieve the method from the stub
    try:
        method = getattr(stub, method_name)
    except AttributeError as exc:
        raise AttributeError(
            f"Method '{method_name}' not found on the dynamic stub. "
            f"Check that the request message descriptor contains the full "
            f"method name 'package.Service.Method'."
        ) from exc

    # Call the method with the provided options
    response = method(
        request,
        timeout=timeout,
        metadata=metadata,
        wait_for_ready=wait_for_ready
    )

    return response