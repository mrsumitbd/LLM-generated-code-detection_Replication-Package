def _center_parent_window(parent: ctk.CTkToplevel, root: ctk.CTk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    parent.update_idletasks()
    parent.withdraw()
    parent.update_idletasks()
    
    if width is None:
        width = parent.winfo_reqwidth()
    if height is None:
        height = parent.winfo_reqheight()
    
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    
    parent.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    parent.deiconify()