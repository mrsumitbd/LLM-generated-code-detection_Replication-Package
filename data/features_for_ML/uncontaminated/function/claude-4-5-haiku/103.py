def apply_format():
    import tkinter as tk
    from tkinter import font as tkFont
    
    root = tk.Tk()
    root.title("Text Formatter")
    root.geometry("500x400")
    
    # Create text widget
    text_widget = tk.Text(root, height=10, width=50, wrap=tk.WORD)
    text_widget.pack(pady=10, padx=10)
    
    # Create frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    def make_bold():
        try:
            current_font = tkFont.Font(font=text_widget.cget("font"))
            bold_font = tkFont.Font(family=current_font.actual("family"), 
                                   size=current_font.actual("size"), 
                                   weight="bold")
            text_widget.tag_configure("bold", font=bold_font)
            text_widget.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def make_italic():
        try:
            current_font = tkFont.Font(font=text_widget.cget("font"))
            italic_font = tkFont.Font(family=current_font.actual("family"), 
                                     size=current_font.actual("size"), 
                                     slant="italic")
            text_widget.tag_configure("italic", font=italic_font)
            text_widget.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def make_underline():
        try:
            current_font = tkFont.Font(font=text_widget.cget("font"))
            underline_font = tkFont.Font(family=current_font.actual("family"), 
                                        size=current_font.actual("size"), 
                                        underline=True)
            text_widget.tag_configure("underline", font=underline_font)
            text_widget.tag_add("underline", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def clear_format():
        text_widget.tag_remove("bold", "1.0", tk.END)
        text_widget.tag_remove("italic", "1.0", tk.END)
        text_widget.tag_remove("underline", "1.0", tk.END)
    
    # Create buttons
    bold_btn = tk.Button(button_frame, text="Bold", command=make_bold, width=10)
    bold_btn.grid(row=0, column=0, padx=5)
    
    italic_btn = tk.Button(button_frame, text="Italic", command=make_italic, width=10)
    italic_btn.grid(row=0, column=1, padx=5)
    
    underline_btn = tk.Button(button_frame, text="Underline", command=make_underline, width=10)
    underline_btn.grid(row=0, column=2, padx=5)
    
    clear_btn = tk.Button(button_frame, text="Clear", command=clear_format, width=10)
    clear_btn.grid(row=0, column=3, padx=5)
    
    root.mainloop()