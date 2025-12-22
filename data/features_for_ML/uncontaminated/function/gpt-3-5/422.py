def log(msg: str, return_line=False, pre_return_line=False, *args, **kwargs):
    if return_line:
        return msg
    if pre_return_line:
        print(msg, *args, **kwargs)
        return
    print(msg, *args, **kwargs)