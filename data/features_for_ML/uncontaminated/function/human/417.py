import kaolin
from threedgrut_playground.utils.kaolin_future.transform import ObjectTransform
import torch

def set_mesh_scale_to_scene(
    scene_scale: torch.Tensor,
    mesh: kaolin.rep.SurfaceMesh,
    transform: ObjectTransform,
    scale_of_new_mesh_to_small_scene=0.5,
) -> None:
    """Automatically scales a mesh to fit appropriately within the scene.

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
    mesh_scale = ((mesh.vertices.max(dim=0)[0] - mesh.vertices.min(dim=0)[0]).cpu()).to(transform.device)
    transform.scale(1.0 / mesh_scale.max())
    if scene_scale.max() > 5.0:  # Don't scale for large scenes
        return
    adjusted_scale = scale_of_new_mesh_to_small_scene * scene_scale.to(transform.device)
    largest_axis_scale = adjusted_scale.max()
    transform.scale(largest_axis_scale)