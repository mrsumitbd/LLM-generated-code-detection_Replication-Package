from typing import Optional

def _center_parent_window(
    parent: "ctk.CTkToplevel",
    root: "ctk.CTk",
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> None:
    """
    Center a CTkToplevel window (`parent`) over its root window (`root`).

    Parameters
    ----------
    parent : ctk.CTkToplevel
        The window to be centered.
    root : ctk.CTk
        The root window that serves as the reference for centering.
    width : Optional[int], default None
        Desired width of the parent window. If None, the current width of
        `parent` is used.
    height : Optional[int], default None
        Desired height of the parent window. If None, the current height of
        `parent` is used.

    Returns
    -------
    None
    """
    # Ensure geometry information is up to date
    root.update_idletasks()
    parent.update_idletasks()

    # Get root geometry
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_w = root.winfo_width()
    root_h = root.winfo_height()

    # Determine parent size
    if width is None:
        parent_w = parent.winfo_width()
        if parent_w <= 1:  # not yet rendered
            parent_w = parent.winfo_reqwidth()
    else:
        parent_w = width

    if height is None:
        parent_h = parent.winfo_height()
        if parent_h <= 1:  # not yet rendered
            parent_h = parent.winfo_reqheight()
    else:
        parent_h = height

    # Compute top-left coordinates to center parent over root
    new_x = root_x + (root_w - parent_w) // 2
    new_y = root_y + (root_h - parent_h) // 2

    # Apply geometry
    parent.geometry(f"{parent_w}x{parent_h}+{new_x}+{new_y}")