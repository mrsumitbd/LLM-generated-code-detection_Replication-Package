def chessboard(*args, **kwargs):
    size = kwargs.get('size', 8)
    symbol1 = kwargs.get('symbol1', '#')
    symbol2 = kwargs.get('symbol2', ' ')
    
    for i in range(size):
        for j in range(size):
            if (i + j) % 2 == 0:
                print(symbol1, end=' ')
            else:
                print(symbol2, end=' ')
        print()