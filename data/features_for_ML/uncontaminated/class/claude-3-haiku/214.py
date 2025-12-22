import os
import re
from tkinter import Tk, Text, Menu, Scrollbar, END, BOTH, VERTICAL, HORIZONTAL, DISABLED, NORMAL

class NanoEditor:
    def __init__(self, filename):
        self.root = Tk()
        self.root.title("NanoEditor")
        self.filename = filename
        self.text_area = Text(self.root, undo=True)
        self.text_area.pack(fill=BOTH, expand=True)
        self.scrollbar_v = Scrollbar(self.root, orient=VERTICAL, command=self.text_area.yview)
        self.scrollbar_v.pack(side='right', fill='y')
        self.scrollbar_h = Scrollbar(self.root, orient=HORIZONTAL, command=self.text_area.xview)
        self.scrollbar_h.pack(side='bottom', fill='x')
        self.text_area.config(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        self.setup_key_bindings()
        self.search_results = []
        self.current_search_index = -1

    def select_syntax_highlight(self):
        pass

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.text_area.delete('1.0', END)
                self.text_area.insert('1.0', file.read())
            self.set_status_message(f"Loaded file: {self.filename}")

    def save_file(self):
        with open(self.filename, 'w') as file:
            file.write(self.get_content())
        self.set_status_message(f"Saved file: {self.filename}")

    def set_status_message(self, message, *args):
        self.root.title(f"NanoEditor - {message.format(*args)}")

    def get_status_text(self):
        return self.root.title().split(" - ")[1]

    def get_message_text(self):
        return self.get_status_text()

    def start_search(self):
        self.search_results = []
        self.current_search_index = -1

    def end_search(self):
        self.search_results = []
        self.current_search_index = -1

    def perform_search(self, query=None):
        if query:
            self.start_search()
            content = self.get_content()
            for match in re.finditer(query, content):
                self.search_results.append(match.start())
            if self.search_results:
                self.current_search_index = 0
                self.jump_to_search_result()
            else:
                self.set_status_message("No matches found for '{}'", query)

    def jump_to_search_result(self, index=None):
        if self.search_results:
            if index is None:
                index = self.current_search_index
            start = f"{self.search_results[index] + 1}.0"
            end = f"{self.search_results[index] + 1 + len(self.perform_search.query)}.0"
            self.text_area.tag_add("search_highlight", start, end)
            self.text_area.tag_config("search_highlight", background="yellow")
            self.text_area.see(start)
            self.current_search_index = index

    def find_next(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.jump_to_search_result()

    def find_previous(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
            self.jump_to_search_result()

    def setup_key_bindings(self):
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-o>", lambda event: self.load_file())
        self.root.bind("<Control-f>", lambda event: self.start_search())
        self.root.bind("<Control-g>", lambda event: self.find_next())
        self.root.bind("<Control-Shift-g>", lambda event: self.find_previous())

    def get_content(self):
        return self.text_area.get("1.0", END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    editor = NanoEditor("example.txt")
    editor.load_file()
    editor.perform_search("example")
    editor.run()