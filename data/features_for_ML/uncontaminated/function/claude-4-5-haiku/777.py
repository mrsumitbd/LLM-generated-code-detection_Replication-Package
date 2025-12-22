def draw_spartan_options(layout: UILayout, props: SpartanOptionsType) -> None:
    """Draw UI elements for Spartan options."""
    
    # Create main column
    col = layout.column(align=True)
    
    # Add header
    col.label(text="Spartan Options", icon='PREFERENCES')
    
    # Add separator
    col.separator()
    
    # Add boolean properties
    row = col.row()
    row.prop(props, "enabled", text="Enable Spartan Mode")
    
    if props.enabled:
        col.separator()
        
        # Add string property
        col.prop(props, "name", text="Name")
        
        # Add integer property
        col.prop(props, "level", text="Level")
        
        # Add enum property
        col.prop(props, "mode", text="Mode")
        
        # Add float property
        col.prop(props, "intensity", text="Intensity", slider=True)
        
        # Add color property
        col.prop(props, "color", text="Color")
        
        col.separator()
        
        # Add advanced options in a box
        box = col.box()
        box.label(text="Advanced Options", icon='MODIFIER')
        
        box.prop(props, "use_advanced", text="Use Advanced Settings")
        
        if props.use_advanced:
            box.prop(props, "threshold", text="Threshold")
            box.prop(props, "iterations", text="Iterations")
    
    col.separator()