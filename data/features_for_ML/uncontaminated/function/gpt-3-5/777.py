def draw_spartan_options(layout: UILayout, props: SpartanOptionsType) -> None:
    for prop in props:
        if prop == 'shield':
            layout.add_image('shield.png')
        elif prop == 'helmet':
            layout.add_image('helmet.png')
        elif prop == 'sword':
            layout.add_image('sword.png')
        elif prop == 'spear':
            layout.add_image('spear.png')