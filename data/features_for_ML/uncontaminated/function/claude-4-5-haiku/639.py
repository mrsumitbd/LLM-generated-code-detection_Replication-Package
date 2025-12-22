def wrap_positions_back_to_box_torch(
    pos: torch.Tensor, lattice_vectors: torch.Tensor
) -> torch.Tensor:
    # transform vector into fractional coordinates
    # lattice_vectors shape: (..., 3, 3)
    # pos shape: (..., 3)
    
    # Compute the inverse of lattice vectors
    lattice_inv = torch.linalg.inv(lattice_vectors)
    
    # Transform to fractional coordinates
    # pos_frac = pos @ lattice_inv.T
    pos_frac = torch.matmul(pos.unsqueeze(-2), lattice_inv.transpose(-2, -1)).squeeze(-2)
    
    # Wrap fractional coordinates back to [0, 1)
    pos_frac = pos_frac - torch.floor(pos_frac)
    
    # Transform back to Cartesian coordinates
    # pos_wrapped = pos_frac @ lattice_vectors.T
    pos_wrapped = torch.matmul(pos_frac.unsqueeze(-2), lattice_vectors.transpose(-2, -1)).squeeze(-2)
    
    return pos_wrapped