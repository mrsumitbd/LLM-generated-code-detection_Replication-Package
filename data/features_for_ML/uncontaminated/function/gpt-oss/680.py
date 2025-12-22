import numpy as np

def get_2d_sincos_pos_embed_from_grid(embed_dim, grid):
    """
    Generate 2‑D sine‑cosine positional embeddings from a grid.

    Parameters
    ----------
    embed_dim : int
        Dimensionality of the final embedding. Must be even.
    grid : tuple or list of two 1‑D arrays
        The first element contains the y‑coordinates, the second the x‑coordinates.
        Each array should be of shape (H,) and (W,) respectively, where H*W is the
        number of positions.

    Returns
    -------
    pos_embed : np.ndarray
        Positional embeddings of shape (H*W, embed_dim).
    """
    # Ensure the embedding dimension is even
    if embed_dim % 2 != 0:
        raise ValueError("embed_dim must be even")

    # Unpack grid
    grid_y, grid_x = grid

    # Flatten coordinates
    grid_y = grid_y.reshape(-1)
    grid_x = grid_x.reshape(-1)

    # Number of positions
    N = grid_y.size

    # Each axis contributes half of the embedding dimension
    dim_each = embed_dim // 2
    # Number of sin/cos pairs per axis
    num_pairs = dim_each // 2

    # Allocate arrays for y and x embeddings
    pos_y = np.zeros((N, dim_each), dtype=np.float32)
    pos_x = np.zeros((N, dim_each), dtype=np.float32)

    # Compute sin/cos embeddings for each axis
    for i in range(num_pairs):
        div_term = 10000 ** (2 * i / dim_each)
        pos_y[:, 2 * i]     = np.sin(grid_y / div_term)
        pos_y[:, 2 * i + 1] = np.cos(grid_y / div_term)
        pos_x[:, 2 * i]     = np.sin(grid_x / div_term)
        pos_x[:, 2 * i + 1] = np.cos(grid_x / div_term)

    # Concatenate y and x embeddings to form the final 2‑D embedding
    pos_embed = np.concatenate([pos_y, pos_x], axis=1)
    return pos_embed