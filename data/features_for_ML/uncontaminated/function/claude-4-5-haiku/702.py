def set_theme():
    # Get username handling bypass modes
    import tkinter as tk
    from tkinter import ttk
    import json
    import os
    
    # Create root window
    root = tk.Tk()
    root.title("Theme Settings")
    root.geometry("400x300")
    
    # Theme options
    themes = ["Light", "Dark", "Auto"]
    
    # Create frame
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Label
    label = ttk.Label(frame, text="Select Theme:", font=("Arial", 12))
    label.grid(row=0, column=0, columnspan=2, pady=10)
    
    # Variable to store selection
    theme_var = tk.StringVar(value="Light")
    
    # Radio buttons
    for i, theme in enumerate(themes):
        radio = ttk.Radiobutton(frame, text=theme, variable=theme_var, value=theme)
        radio.grid(row=i+1, column=0, sticky=tk.W, pady=5)
    
    # Save button
    def save_theme():
        selected_theme = theme_var.get()
        config = {"theme": selected_theme}
        
        # Save to file
        config_file = "theme_config.json"
        with open(config_file, "w") as f:
            json.dump(config, f)
        
        root.destroy()
    
    save_button = ttk.Button(frame, text="Save", command=save_theme)
    save_button.grid(row=len(themes)+1, column=0, pady=20)
    
    root.mainloop()