import torch

def wrap_positions_back_to_box_torch(pos: torch.Tensor, lattice_vectors: torch.Tensor) -> torch.Tensor:
    fractional_coords = torch.linalg.solve(lattice_vectors.t(), pos.t()).t()
    fractional_coords = fractional_coords - torch.floor(fractional_coords)
    wrapped_coords = torch.matmul(fractional_coords, lattice_vectors)
    return wrapped_coords