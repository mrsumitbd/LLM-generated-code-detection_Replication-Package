def _center_parent_window(parent: ctk.CTkToplevel, root: ctk.CTk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    if width is None or height is None:
        width, height = parent.winfo_reqwidth(), parent.winfo_reqheight()

    parent_width = root.winfo_width()
    parent_height = root.winfo_height()

    x = (parent_width // 2) - (width // 2)
    y = (parent_height // 2) - (height // 2)

    parent.geometry(f"{width}x{height}+{x}+{y}")