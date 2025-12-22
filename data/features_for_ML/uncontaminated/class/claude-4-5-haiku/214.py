class NanoEditor:

    def __init__(self, filename):
        self.filename = filename
        self.content = ""
        self.status_message = ""
        self.message_text = ""
        self.syntax_highlight = None
        self.search_active = False
        self.search_query = ""
        self.search_results = []
        self.current_search_index = -1
        self.key_bindings = {}

    def select_syntax_highlight(self):
        if self.filename:
            ext = self.filename.split('.')[-1].lower() if '.' in self.filename else ""
            syntax_map = {
                'py': 'python',
                'js': 'javascript',
                'java': 'java',
                'c': 'c',
                'cpp': 'cpp',
                'txt': 'text',
                'md': 'markdown',
                'html': 'html',
                'css': 'css',
                'json': 'json'
            }
            self.syntax_highlight = syntax_map.get(ext, 'text')
        else:
            self.syntax_highlight = 'text'

    def load_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.select_syntax_highlight()
            self.set_status_message("File loaded successfully")
            return True
        except FileNotFoundError:
            self.set_status_message("File not found: %s", self.filename)
            return False
        except Exception as e:
            self.set_status_message("Error loading file: %s", str(e))
            return False

    def save_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(self.content)
            self.set_status_message("File saved successfully")
            return True
        except Exception as e:
            self.set_status_message("Error saving file: %s", str(e))
            return False

    def set_status_message(self, message, *args):
        if args:
            self.status_message = message % args
        else:
            self.status_message = message
        self.message_text = self.status_message

    def get_status_text(self):
        return self.status_message

    def get_message_text(self):
        return self.message_text

    def start_search(self):
        self.search_active = True
        self.search_query = ""
        self.search_results = []
        self.current_search_index = -1
        self.set_status_message("Search mode active (type query)")

    def end_search(self):
        self.search_active = False
        self.search_query = ""
        self.search_results = []
        self.current_search_index = -1
        self.set_status_message("Search mode ended")

    def perform_search(self, query=None):
        if query is not None:
            self.search_query = query
        
        if not self.search_query:
            self.search_results = []
            self.current_search_index = -1
            return
        
        self.search_results = []
        query_lower = self.search_query.lower()
        content_lower = self.content.lower()
        
        start = 0
        while True:
            pos = content_lower.find(query_lower, start)
            if pos == -1:
                break
            self.search_results.append(pos)
            start = pos + 1
        
        if self.search_results:
            self.current_search_index = 0
            self.set_status_message("Found %d matches", len(self.search_results))
        else:
            self.current_search_index = -1
            self.set_status_message("No matches found")

    def jump_to_search_result(self, index=None):
        if not self.search_results:
            return -1
        
        if index is not None:
            if 0 <= index < len(self.search_results):
                self.current_search_index = index
                return self.search_results[index]
        elif self.current_search_index >= 0:
            return self.search_results[self.current_search_index]
        
        return -1

    def find_next(self):
        if not self.search_results:
            return -1
        
        self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
        return self.search_results[self.current_search_index]

    def find_previous(self):
        if not self.search_results:
            return -1
        
        self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
        return self.search_results[self.current_search_index]

    def setup_key_bindings(self):
        self.key_bindings = {
            'ctrl_s': self.save_file,
            'ctrl_x': self.end_search,
            'ctrl_f': self.start_search,
            'ctrl_n': self.find_next,
            'ctrl_p': self.find_previous
        }

    def get_content(self):
        return self.content

    def run(self):
        self.load_file()
        self.setup_key_bindings()
        self.select_syntax_highlight()
        return True