def get_2d_sincos_pos_embed_from_grid(embed_dim, grid):
    import math
    import numpy as np
    
    embed_pos = np.zeros((grid.shape[0], grid.shape[1], embed_dim))
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            for d in range(embed_dim // 2):
                embed_pos[i, j, 2*d] = math.sin(grid[i, j] / 10000 ** (2*d / embed_dim))
                embed_pos[i, j, 2*d + 1] = math.cos(grid[i, j] / 10000 ** (2*d / embed_dim))
    
    return embed_pos