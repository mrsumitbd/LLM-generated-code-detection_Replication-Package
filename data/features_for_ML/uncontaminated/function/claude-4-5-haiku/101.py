def _split_args_kwargs_data_proto(chunks, *args, **kwargs):
    """
    Split args and kwargs into data and proto components.
    
    This function separates positional and keyword arguments into two groups:
    - data: regular arguments that should be passed as-is
    - proto: arguments that are protocol buffer messages
    
    Args:
        chunks: Number of chunks to process
        *args: Variable length argument list
        **kwargs: Arbitrary keyword arguments
    
    Returns:
        A tuple of (data_args, data_kwargs, proto_args, proto_kwargs)
    """
    data_args = []
    proto_args = []
    data_kwargs = {}
    proto_kwargs = {}
    
    # Process positional arguments
    for arg in args:
        # Check if argument is a protocol buffer message
        # Protocol buffers have a DESCRIPTOR attribute
        if hasattr(arg, 'DESCRIPTOR'):
            proto_args.append(arg)
        else:
            data_args.append(arg)
    
    # Process keyword arguments
    for key, value in kwargs.items():
        # Check if value is a protocol buffer message
        if hasattr(value, 'DESCRIPTOR'):
            proto_kwargs[key] = value
        else:
            data_kwargs[key] = value
    
    return data_args, data_kwargs, proto_args, proto_kwargs