def guess_block_id(name):
    """
    Guess a block ID from a block name.

    The function normalises the input name (lower‑case, strip whitespace,
    replace spaces with underscores) and looks it up in a small
    dictionary of common block names.  If the name is not found, None
    is returned.

    Parameters
    ----------
    name : str
        The block name to look up.

    Returns
    -------
    int or None
        The corresponding block ID, or None if the name is unknown.
    """
    # Normalise the name
    if not isinstance(name, str):
        return None
    key = name.strip().lower().replace(" ", "_")

    # A small mapping of common block names to IDs (Minecraft 1.7+ style)
    _BLOCK_MAP = {
        "air": 0,
        "stone": 1,
        "grass": 2,
        "dirt": 3,
        "cobblestone": 4,
        "planks": 5,
        "sapling": 6,
        "bedrock": 7,
        "water": 8,
        "lava": 9,
        "sand": 12,
        "gravel": 13,
        "gold_ore": 14,
        "iron_ore": 15,
        "coal_ore": 16,
        "log": 17,
        "leaves": 18,
        "sponge": 19,
        "glass": 20,
        "lapis_ore": 21,
        "lapis_block": 22,
        "dispenser": 23,
        "sandstone": 24,
        "note_block": 25,
        "bed": 26,
        "golden_rail": 27,
        "detector_rail": 28,
        "sticky_piston": 29,
        "cobweb": 30,
        "tallgrass": 31,
        "deadbush": 32,
        "piston": 33,
        "piston_head": 34,
        "wool": 35,
        "yellow_wool": 36,
        "orange_wool": 37,
        "magenta_wool": 38,
        "light_blue_wool": 39,
        "cyan_wool": 40,
        "purple_wool": 41,
        "blue_wool": 42,
        "brown_wool": 43,
        "green_wool": 44,
        "red_wool": 45,
        "black_wool": 46,
        "dandelion": 47,
        "poppy": 48,
        "brown_mushroom": 49,
        "red_mushroom": 50,
        "gold_block": 51,
        "iron_block": 52,
        "double_stone_slab": 53,
        "stone_slab": 54,
        "brick_block": 55,
        "tnt": 56,
        "bookshelf": 57,
        "mossy_cobblestone": 58,
        "obsidian": 59,
        "torch": 61,
        "fire": 62,
        "spawner": 65,
        "oak_stairs": 67,
        "chest": 54,  # Note: chest shares ID with stone_slab in this simplified map
    }

    return _BLOCK_MAP.get(key)