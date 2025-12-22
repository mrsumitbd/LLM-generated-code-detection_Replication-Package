import torch
import kaolin

def set_mesh_scale_to_scene(
    scene_scale: torch.Tensor,
    mesh: kaolin.rep.SurfaceMesh,
    transform: ObjectTransform,
    scale_of_new_mesh_to_small_scene=0.5,
) -> None:
    max_dim = scene_scale.max()
    if max_dim <= 5.0:
        scale_factor = scale_of_new_mesh_to_small_scene * max_dim / mesh.vertices.abs().max()
    else:
        scale_factor = 1.0 / mesh.vertices.abs().max()
    
    mesh.vertices *= scale_factor
    transform.scale *= scale_factor