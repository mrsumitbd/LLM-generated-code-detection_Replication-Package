def create_text_entry(name: str):
    import tkinter as tk
    
    root = tk.Tk()
    root.title(name)
    root.geometry("400x300")
    
    label = tk.Label(root, text=f"Enter text for {name}:")
    label.pack(pady=10)
    
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=10)
    
    def on_submit():
        entered_text = text_entry.get()
        print(f"Entered text: {entered_text}")
        root.destroy()
    
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)
    
    root.mainloop()