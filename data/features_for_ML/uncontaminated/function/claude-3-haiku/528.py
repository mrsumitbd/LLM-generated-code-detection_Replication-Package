def chessboard(*args, **kwargs):
    """
    Generates a chessboard-like pattern in the console.

    Parameters:
    *args (int): The size of the chessboard (width and height). If only one argument is provided, it is used for both width and height.
    **kwargs:
        - color1 (str): The color of the light squares (default is 'white').
        - color2 (str): The color of the dark squares (default is 'black').
        - separator (str): The character used to separate the squares (default is ' ').

    Returns:
    None
    """
    if args:
        if len(args) == 1:
            width = height = args[0]
        else:
            width, height = args
    else:
        width = height = 8

    color1 = kwargs.get('color1', 'white')
    color2 = kwargs.get('color2', 'black')
    separator = kwargs.get('separator', ' ')

    for y in range(height):
        row = []
        for x in range(width):
            if (x + y) % 2 == 0:
                row.append(f"\033[{color1}m{separator}\033[0m")
            else:
                row.append(f"\033[{color2}m{separator}\033[0m")
        print(''.join(row))