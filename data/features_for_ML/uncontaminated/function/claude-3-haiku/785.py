import torch

def model_matrix(self):
    """
    Returns:
        (torch.Tensor): a 4x4 model matrix which encodes the complete transform of the object from local
        coordinates to world coordinates.
    """
    translation_matrix = torch.eye(4)
    translation_matrix[:3, 3] = self.position

    rotation_matrix = torch.eye(4)
    rotation_matrix[:3, :3] = self.rotation.to_matrix()

    scale_matrix = torch.eye(4)
    scale_matrix[:3, :3] = torch.diag(self.scale)

    model_matrix = translation_matrix @ rotation_matrix @ scale_matrix

    return model_matrix