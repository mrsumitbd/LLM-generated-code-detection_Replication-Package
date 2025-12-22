import torch

def wrap_positions_back_to_box_torch(pos: torch.Tensor, lattice_vectors: torch.Tensor) -> torch.Tensor:
    # transform vector into fractional coordinates
    frac_coords = torch.matmul(pos, torch.inverse(lattice_vectors))
    
    # wrap fractional coordinates back to the box
    frac_coords = frac_coords - torch.floor(frac_coords)
    
    # transform back to cartesian coordinates
    wrapped_pos = torch.matmul(frac_coords, lattice_vectors)
    
    return wrapped_pos