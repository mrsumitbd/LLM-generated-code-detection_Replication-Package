def model_matrix(self):
    """
    Returns:
        (torch.Tensor): a 4x4 model matrix which encodes the complete transform of the object from local
        coordinates to world coordinates.
    """
    import torch
    
    # Create translation matrix
    translation = torch.eye(4)
    translation[0, 3] = self.position[0]
    translation[1, 3] = self.position[1]
    translation[2, 3] = self.position[2]
    
    # Create rotation matrix from quaternion
    qx, qy, qz, qw = self.quaternion
    rotation = torch.tensor([
        [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy), 0],
        [2*(qx*qy + qw*qz), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qw*qx), 0],
        [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), 1 - 2*(qx**2 + qy**2), 0],
        [0, 0, 0, 1]
    ], dtype=torch.float32)
    
    # Create scale matrix
    scale = torch.eye(4)
    scale[0, 0] = self.scale[0]
    scale[1, 1] = self.scale[1]
    scale[2, 2] = self.scale[2]
    
    # Combine: Translation * Rotation * Scale
    model = translation @ rotation @ scale
    
    return model