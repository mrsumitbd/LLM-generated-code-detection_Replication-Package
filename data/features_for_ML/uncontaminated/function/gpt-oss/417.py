import torch
import kaolin
from kaolin.rep import SurfaceMesh
from kaolin.transforms import ObjectTransform

def set_mesh_scale_to_scene(
    scene_scale: torch.Tensor,
    mesh: kaolin.rep.SurfaceMesh,
    transform: ObjectTransform,
    scale_of_new_mesh_to_small_scene: float = 0.5,
) -> None:
    """
    Automatically scales a mesh to fit appropriately within the scene.

    This function is a heuristic that applies a two-step scaling process:
    1. Normalizes mesh to unit size by dividing by its largest dimension
    2. For small scenes (max dimension ≤ 5.0), scales the mesh to a proportion
       of the scene size

    Args:
        scene_scale (torch.Tensor): Overall scene dimensions of shape (3,)
        mesh (kaolin.rep.SurfaceMesh): Mesh to be scaled
        transform (ObjectTransform): Transform object to apply scaling to
        scale_of_new_mesh_to_small_scene (float, optional): For small scenes,
            mesh will be scaled to this fraction of scene size. Defaults to 0.5.

    Note:
        - Large scenes (max dimension > 5.0) only get unit normalization
        - Small scenes get additional scaling relative to scene size
        - All scaling is uniform (preserves mesh proportions)
        - Scaling is applied through the transform object
    """
    # Ensure we are working with float tensors
    verts = mesh.vertices.to(torch.float32)

    # Compute bounding box of the mesh
    min_bounds = verts.min(0).values
    max_bounds = verts.max(0).values
    bbox_size = max_bounds - min_bounds

    # Largest dimension of the mesh
    mesh_max_dim = bbox_size.max().item()

    # Unit normalization factor
    if mesh_max_dim > 0:
        unit_scale_factor = 1.0 / mesh_max_dim
    else:
        unit_scale_factor = 1.0

    # Determine if the scene is considered "small"
    scene_max_dim = scene_scale.max().item()
    if scene_max_dim <= 5.0:
        # Scale mesh to a fraction of the scene size
        target_scale = scale_of_new_mesh_to_small_scene * scene_max_dim
    else:
        target_scale = 1.0

    # Total uniform scaling factor
    total_scale = unit_scale_factor * target_scale

    # Apply scaling via the transform object
    transform.scale(total_scale)