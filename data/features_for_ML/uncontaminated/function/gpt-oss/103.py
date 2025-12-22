def apply_format():
    import sys
    data = sys.stdin.read().splitlines()
    if not data:
        return
    fmt = data[0]
    if len(data) < 2:
        print(fmt)
        return
    try:
        n = int(data[1])
    except ValueError:
        # If second line is not an integer, treat all remaining lines as arguments
        args = data[1:]
        try:
            print(fmt.format(*args))
        except Exception:
            print(fmt)
        return
    args = data[2:2 + n]
    try:
        print(fmt.format(*args))
    except Exception:
        print(fmt)