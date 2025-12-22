def transpose(tensor):
    """
    Transpose a nested list (tensor) by swapping its first two dimensions.
    For a 2‑D list, this is the usual matrix transpose.
    For higher‑dimensional tensors, the function recursively transposes
    the inner lists after swapping the first two axes.
    """
    # Base case: not a list or empty list
    if not isinstance(tensor, list) or len(tensor) == 0:
        return tensor

    # If all elements are lists, we can attempt a 2‑D transpose
    if all(isinstance(x, list) for x in tensor):
        # Ensure the tensor is rectangular
        row_len = len(tensor[0])
        for row in tensor:
            if len(row) != row_len:
                raise ValueError("All rows must have the same length")

        # Transpose the first two dimensions
        transposed = []
        for i in range(row_len):
            new_row = []
            for j in range(len(tensor)):
                new_row.append(tensor[j][i])
            transposed.append(new_row)

        # Recursively transpose inner lists
        return [transpose(row) for row in transposed]

    # If the elements are not lists, we are at the innermost level
    return tensor