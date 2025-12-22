def _split_args_kwargs_data_proto(chunks, *args, **kwargs):
    args_list = list(args)
    kwargs_dict = dict(kwargs)
    return chunks, args_list, kwargs_dict