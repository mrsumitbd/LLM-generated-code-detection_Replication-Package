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
    # Normalize mesh to unit size
    mesh_scale = torch.max(mesh.vertices.abs(), dim=0).values
    mesh.vertices /= mesh_scale

    # Determine if scene is small and apply additional scaling if so
    max_scene_dim = torch.max(scene_scale)
    if max_scene_dim <= 5.0:
        mesh_scale *= scale_of_new_mesh_to_small_scene * scene_scale / max_scene_dim

    # Apply the scaling to the transform
    transform.scale(mesh_scale)