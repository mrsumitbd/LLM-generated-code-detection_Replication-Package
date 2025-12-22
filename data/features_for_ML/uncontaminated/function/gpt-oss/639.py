import torch

def wrap_positions_back_to_box_torch(
    pos: torch.Tensor, lattice_vectors: torch.Tensor
) -> torch.Tensor:
    """
    Wrap Cartesian positions back into the unit cell defined by `lattice_vectors`.

    Parameters
    ----------
    pos : torch.Tensor
        Cartesian coordinates of shape (..., 3).
    lattice_vectors : torch.Tensor
        Lattice vectors of shape (3, 3) where each row is a lattice vector.

    Returns
    -------
    torch.Tensor
        Wrapped Cartesian coordinates of the same shape as `pos`.
    """
    # Ensure tensors are on the same device and dtype
    device = pos.device
    dtype = pos.dtype
    lattice_vectors = lattice_vectors.to(device=device, dtype=dtype)

    # Compute inverse of the lattice matrix (rows are lattice vectors)
    inv_lattice = torch.linalg.inv(lattice_vectors)

    # Convert Cartesian to fractional coordinates
    frac = pos @ inv_lattice.T

    # Wrap fractional coordinates into [0, 1)
    frac_wrapped = torch.remainder(frac, 1.0)

    # Convert back to Cartesian coordinates
    wrapped_pos = frac_wrapped @ lattice_vectors

    return wrapped_pos