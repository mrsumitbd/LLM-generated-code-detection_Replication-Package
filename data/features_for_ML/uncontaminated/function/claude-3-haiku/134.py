def show_tooltip():
    import tkinter as tk

    root = tk.Tk()
    root.title("Tooltip Example")

    label = tk.Label(root, text="Hover over me to see the tooltip")
    label.pack(pady=20)

    def show_tip(event):
        x, y = event.x + label.winfo_rootx() + 10, event.y + label.winfo_rooty() + 10
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide_tip(event):
        tooltip.withdraw()

    tooltip = tk.Toplevel(root)
    tooltip.overrideredirect(True)
    tooltip_label = tk.Label(tooltip, text="This is a tooltip", padx=5, pady=2)
    tooltip_label.pack()
    tooltip.withdraw()

    label.bind("<Enter>", show_tip)
    label.bind("<Leave>", hide_tip)

    root.mainloop()