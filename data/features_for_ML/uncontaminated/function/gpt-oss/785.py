import torch

def model_matrix(self):
    """
    Returns:
        (torch.Tensor): a 4x4 model matrix which encodes the complete transform of the object
        from local coordinates to world coordinates.
    """
    # Ensure tensors
    pos = torch.as_tensor(self.position, dtype=torch.float32)
    scale = torch.as_tensor(self.scale, dtype=torch.float32)

    # Rotation matrix
    if getattr(self, "rotation", None) is None:
        R = torch.eye(4, dtype=torch.float32)
    else:
        rot = torch.as_tensor(self.rotation, dtype=torch.float32)
        if rot.shape == (4,):  # quaternion [w, x, y, z]
            w, x, y, z = rot
            R = torch.tensor(
                [
                    [1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w, 0],
                    [2 * x * y + 2 * z * w, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * x * w, 0],
                    [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x * x - 2 * y * y, 0],
                    [0, 0, 0, 1],
                ],
                dtype=torch.float32,
            )
        elif rot.shape == (3,):  # Euler angles (roll, pitch, yaw) in radians
            roll, pitch, yaw = rot
            Rx = torch.tensor(
                [
                    [1, 0, 0, 0],
                    [0, torch.cos(roll), -torch.sin(roll), 0],
                    [0, torch.sin(roll), torch.cos(roll), 0],
                    [0, 0, 0, 1],
                ],
                dtype=torch.float32,
            )
            Ry = torch.tensor(
                [
                    [torch.cos(pitch), 0, torch.sin(pitch), 0],
                    [0, 1, 0, 0],
                    [-torch.sin(pitch), 0, torch.cos(pitch), 0],
                    [0, 0, 0, 1],
                ],
                dtype=torch.float32,
            )
            Rz = torch.tensor(
                [
                    [torch.cos(yaw), -torch.sin(yaw), 0, 0],
                    [torch.sin(yaw), torch.cos(yaw), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=torch.float32,
            )
            R = Rz @ Ry @ Rx
        else:
            raise ValueError("Rotation must be a quaternion (4,) or Euler angles (3,)")

    # Scale matrix
    S = torch.diag(torch.cat([scale, torch.tensor([1.0], dtype=torch.float32)]))

    # Translation matrix
    T = torch.eye(4, dtype=torch.float32)
    T[:3, 3] = pos

    # Combine transformations: world = T * R * S
    return T @ R @ S