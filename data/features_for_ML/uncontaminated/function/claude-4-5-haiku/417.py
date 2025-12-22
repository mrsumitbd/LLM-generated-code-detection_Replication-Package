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
    # Get mesh vertices and compute bounding box
    vertices = mesh.vertices
    min_coords = torch.min(vertices, dim=0)[0]
    max_coords = torch.max(vertices, dim=0)[0]
    mesh_size = max_coords - min_coords
    
    # Step 1: Normalize mesh to unit size by dividing by largest dimension
    max_mesh_dimension = torch.max(mesh_size)
    scale_factor = 1.0 / max_mesh_dimension
    
    # Step 2: For small scenes, scale relative to scene size
    max_scene_dimension = torch.max(scene_scale)
    if max_scene_dimension <= 5.0:
        # Small scene: scale mesh to a proportion of scene size
        scale_factor *= max_scene_dimension * scale_of_new_mesh_to_small_scene
    
    # Apply scaling through transform
    transform.scale = scale_factor