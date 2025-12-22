def _render() -> str:
    import inspect
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None:
        return ""
    
    caller_frame = frame.f_back
    caller_locals = caller_frame.f_locals
    caller_globals = caller_frame.f_globals
    
    # Get the source code of the calling line
    try:
        import linecache
        filename = caller_frame.f_code.co_filename
        lineno = caller_frame.f_lineno
        line = linecache.getline(filename, lineno).strip()
    except:
        return ""
    
    # Extract the argument from the function call
    if "_render()" in line:
        # Find what's being passed to _render
        start = line.find("_render(")
        if start != -1:
            start += len("_render(")
            end = line.rfind(")")
            if end != -1:
                arg_str = line[start:end].strip()
                try:
                    result = eval(arg_str, caller_globals, caller_locals)
                    return str(result)
                except:
                    return arg_str
    
    return ""