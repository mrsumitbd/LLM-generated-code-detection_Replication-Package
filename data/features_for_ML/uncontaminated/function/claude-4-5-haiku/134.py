def show_tooltip():
    import tkinter as tk
    from tkinter import ttk
    
    root = tk.Tk()
    root.title("Tooltip Example")
    root.geometry("300x200")
    
    class ToolTip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tooltip = None
            self.widget.bind("<Enter>", self.on_enter)
            self.widget.bind("<Leave>", self.on_leave)
        
        def on_enter(self, event):
            if self.tooltip:
                return
            
            x = event.x_root + 10
            y = event.y_root + 10
            
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                self.tooltip,
                text=self.text,
                background="lightyellow",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Arial", 9)
            )
            label.pack()
        
        def on_leave(self, event):
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
    
    button = tk.Button(root, text="Hover over me", padx=20, pady=10)
    button.pack(pady=50)
    
    tooltip = ToolTip(button, "This is a tooltip!")
    
    root.mainloop()