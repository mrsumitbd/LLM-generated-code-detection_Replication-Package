def log(msg: str, return_line=False, pre_return_line=False, *args, **kwargs):
    if pre_return_line:
        print()
    print(msg, *args, **kwargs)
    if return_line:
        print()