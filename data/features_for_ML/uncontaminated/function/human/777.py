from bpy.types import Context, PropertyGroup, UILayout

def draw_spartan_options(layout: UILayout, props: SpartanOptionsType) -> None:
    ocgd_header, ocgd_body = layout.panel("VIEW3D_PT_import_ocgd", default_closed=True)
    ocgd_header.label(icon="ARMATURE_DATA", text="Import Spartan")
    if ocgd_body:
        ocgd_body.prop(props, "use_purp_rig")
        ocgd_opts = ocgd_body.box()
        ocgd_opts.prop(props, "import_specific_core")
        if props.import_specific_core:
            ocgd_opts.prop(props, "core")

        ocgd_opts.prop(props, "import_names")
        _ = ocgd_opts.operator("ekur.importspartan")
        vanity_opts = ocgd_body.box()
        vanity_opts.prop(props, "body_type")
        vanity_opts.prop(props, "left_arm")
        vanity_opts.prop(props, "right_arm")
        vanity_opts.prop(props, "left_leg")
        vanity_opts.prop(props, "right_leg")
        vanity_opts.prop(props, "gamertag")
        _ = vanity_opts.operator("ekur.importvanity")