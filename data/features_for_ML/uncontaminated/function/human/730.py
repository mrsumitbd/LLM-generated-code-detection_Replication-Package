def asset_creation_strategy() -> str:
    """Defines the preferred strategy for creating assets in Blender"""
    return """When creating 3D content in Blender, always start by checking if integrations are available:

    0. Before anything, always check the scene from get_scene_info()
    1. First use the following tools to verify if the following integrations are enabled:
        1. PolyHaven
            Use get_polyhaven_status() to verify its status
            If PolyHaven is enabled:
            - For objects/models: Use download_polyhaven_asset() with asset_type="models"
            - For materials/textures: Use download_polyhaven_asset() with asset_type="textures"
            - For environment lighting: Use download_polyhaven_asset() with asset_type="hdris"
       
    2. If all integrations are disabled or when falling back to basic tools:
       - create_object() for basic primitives (CUBE, SPHERE, CYLINDER, etc.)
       - set_material() for basic colors and materials
    
    3. When including an object into scene, ALWAYS make sure that the name of the object is meanful.

    4. Always check the world_bounding_box for each item so that:
        - Ensure that all objects that should not be clipping are not clipping.
        - Items have right spatial relationship.
    
    5. After giving the tool location/scale/rotation information (via create_object() and modify_object()),
        double check the related object's location, scale, rotation, and world_bounding_box using get_object_info(),
        so that the object is in the desired location.

    Only fall back to basic creation tools when:
    - PolyHaven is disabled
    - A simple primitive is explicitly requested
    - No suitable PolyHaven asset exists
    - The task specifically requires a basic material/color
    """