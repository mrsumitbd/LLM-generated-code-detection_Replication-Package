import torch

def wrap_positions_back_to_box_torch(
    pos: torch.Tensor, lattice_vectors: torch.Tensor
) -> torch.Tensor:
    # transform vector into fractional coordinates
    fractional_coords = cart2frac_torch(pos, lattice_vectors)

    # adjust the positions
    # adjust the vector
    fractional_coords[fractional_coords > 1.0] -= 1.0
    fractional_coords[fractional_coords < 0.0] += 1.0

    # transform back and return
    return frac2cart_torch(fractional_coords, lattice_vectors)