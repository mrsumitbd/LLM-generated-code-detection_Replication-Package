def _split_args_kwargs_data_proto(chunks, *args, **kwargs):
    args_list = list(args)
    kwargs_dict = dict(kwargs)
    data_proto = chunks.pop(0)
    return args_list, kwargs_dict, data_proto