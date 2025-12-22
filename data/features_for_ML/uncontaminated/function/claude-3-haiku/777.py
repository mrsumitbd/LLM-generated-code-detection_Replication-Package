def draw_spartan_options(layout: UILayout, props: SpartanOptionsType) -> None:
    row = layout.row()
    row.prop(props, "show_spartan_options")

    if props.show_spartan_options:
        box = layout.box()
        box.label(text="Spartan Options")

        row = box.row()
        row.prop(props, "spartan_size")
        row.prop(props, "spartan_color")

        row = box.row()
        row.prop(props, "spartan_speed")
        row.prop(props, "spartan_jump_height")

        row = box.row()
        row.prop(props, "spartan_health")
        row.prop(props, "spartan_shield")