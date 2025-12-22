def run_find_words(solution_class: type, board: list[list[str]], words: list[str]):
    """
    Instantiate the provided solution class and invoke its `findWords` method
    with the given board and words. The result is returned directly.

    Parameters
    ----------
    solution_class : type
        A class that implements a `findWords(self, board, words)` method.
    board : list[list[str]]
        2D list representing the character board.
    words : list[str]
        List of words to search for in the board.

    Returns
    -------
    list[str]
        The list of words found in the board as returned by the solution.
    """
    # Instantiate the solution class
    solution = solution_class()
    # Call the findWords method and return its result
    return solution.findWords(board, words)