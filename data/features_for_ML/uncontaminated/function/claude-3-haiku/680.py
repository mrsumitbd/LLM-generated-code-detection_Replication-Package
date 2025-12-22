import numpy as np

def get_2d_sincos_pos_embed_from_grid(embed_dim, grid):
    """
    Construct 2D position embedding from a grid.

    Args:
        embed_dim (int): Embedding dimension.
        grid (tuple): A tuple of (H, W) representing the height and width of the 2D grid.

    Returns:
        np.ndarray: 2D position embedding of shape (H, W, embed_dim).
    """
    h, w = grid
    grid_y, grid_x = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    grid_y = grid_y.flatten()
    grid_x = grid_x.flatten()

    dim_t = np.arange(embed_dim, dtype=np.float32)
    dim_t = 10000 ** (2 * (dim_t // 2) / embed_dim)

    pos_x = grid_x[:, None] / dim_t
    pos_y = grid_y[:, None] / dim_t

    pos_x = np.stack((np.sin(pos_x[:, 0::2]), np.cos(pos_x[:, 1::2])), axis=2).flatten(1)
    pos_y = np.stack((np.sin(pos_y[:, 0::2]), np.cos(pos_y[:, 1::2])), axis=2).flatten(1)

    pos_embed = np.concatenate((pos_y, pos_x), axis=1)
    pos_embed = pos_embed.reshape(h, w, embed_dim)
    return pos_embed