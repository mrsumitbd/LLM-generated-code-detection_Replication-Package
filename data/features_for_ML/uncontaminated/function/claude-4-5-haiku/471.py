def _center_parent_window(parent: ctk.CTkToplevel, root: ctk.CTk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    parent.update_idletasks()
    
    if width is None:
        width = parent.winfo_width()
    if height is None:
        height = parent.winfo_height()
    
    root.update_idletasks()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    x = root_x + (root_width - width) // 2
    y = root_y + (root_height - height) // 2
    
    parent.geometry(f"{width}x{height}+{x}+{y}")