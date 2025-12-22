from typing import Optional, List, Callable
import customtkinter as ctk

def _center_parent_window(parent: ctk.CTkToplevel, root: ctk.CTk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    root.update_idletasks()
    parent.update_idletasks()
    
    width = width or parent.winfo_width()
    height = height or parent.winfo_height()
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2
    parent.geometry(f"{width}x{height}+{x}+{y}")