def get_task_str(task_type_ind, object_ind, receptacle_ind=None, toggle_ind=None, mrecep_ind=None):
    """
    Construct a human‑readable task description from index values.

    Parameters
    ----------
    task_type_ind : int
        Index indicating the type of task (e.g., pick, place, toggle, move).
    object_ind : int
        Index of the object involved in the task.
    receptacle_ind : int, optional
        Index of the receptacle (e.g., sink, fridge) for pick/place tasks.
    toggle_ind : int, optional
        Index of the toggleable item (e.g., light, door) for toggle tasks.
    mrecep_ind : int, optional
        Index of a multi‑receptacle (e.g., drawer, cabinet) for move tasks.

    Returns
    -------
    str
        A string describing the task, e.g. "pick cup from sink".
    """
    # Basic mappings – these can be extended or replaced by external look‑ups.
    task_map = {
        0: "pick",
        1: "place",
        2: "toggle",
        3: "move",
    }
    object_map = {
        0: "cup",
        1: "bottle",
        2: "plate",
        3: "spoon",
        4: "book",
    }
    receptacle_map = {
        0: "sink",
        1: "fridge",
        2: "counter",
        3: "drawer",
        4: "cabinet",
    }
    toggle_map = {
        0: "light",
        1: "door",
        2: "oven",
    }
    mrecep_map = {
        0: "drawer",
        1: "cabinet",
        2: "shelf",
    }

    # Resolve indices to names, falling back to a generic placeholder.
    verb = task_map.get(task_type_ind, f"task{task_type_ind}")
    obj = object_map.get(object_ind, f"obj{object_ind}") if object_ind is not None else None
    rec = receptacle_map.get(receptacle_ind, f"rec{receptacle_ind}") if receptacle_ind is not None else None
    tog = toggle_map.get(toggle_ind, f"toggle{toggle_ind}") if toggle_ind is not None else None
    mrec = mrecep_map.get(mrecep_ind, f"mrec{mrecep_ind}") if mrecep_ind is not None else None

    # Build the description based on the task type and available components.
    if task_type_ind == 2 and tog is not None:
        # Toggle task – only the toggle item is relevant.
        return f"{verb} {tog}"
    if task_type_ind in (0, 1) and obj is not None and rec is not None:
        # Pick or place – object and receptacle are required.
        preposition = "from" if task_type_ind == 0 else "on"
        return f"{verb} {obj} {preposition} {rec}"
    if task_type_ind == 3 and obj is not None and mrec is not None:
        # Move task – object and multi‑receptacle are required.
        return f"{verb} {obj} to {mrec}"

    # Fallback: concatenate all available parts.
    parts = [verb]
    if obj:
        parts.append(obj)
    if rec:
        parts.append(rec)
    if tog:
        parts.append(tog)
    if mrec:
        parts.append(mrec)
    return " ".join(parts)