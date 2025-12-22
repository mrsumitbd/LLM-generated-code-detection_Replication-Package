def run_find_words(solution_class: type, board: list[list[str]], words: list[str]):
    solution = solution_class()
    result = solution.findWords(board, words)
    return result