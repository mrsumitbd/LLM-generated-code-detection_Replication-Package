import curses
import os
import re
import sys
from typing import List, Tuple, Optional


class NanoEditor:
    def __init__(self, filename: str):
        self.filename = filename
        self.buffer: List[str] = []
        self.syntax = None
        self.status_msg = ""
        self.message = ""
        self.search_mode = False
        self.search_query = ""
        self.search_results: List[Tuple[int, int]] = []
        self.search_index = 0
        self.cursor_row = 0
        self.cursor_col = 0
        self.top_line = 0  # For scrolling
        self.load_file()
        self.select_syntax_highlight()

    def select_syntax_highlight(self):
        _, ext = os.path.splitext(self.filename)
        self.syntax = ext.lower()

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.buffer = [line.rstrip("\n") for line in f]
        else:
            self.buffer = [""]
        self.cursor_row = 0
        self.cursor_col = 0

    def save_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for line in self.buffer:
                f.write(line + "\n")
        self.set_status_message("Saved %s", self.filename)

    def set_status_message(self, message: str, *args):
        self.status_msg = message % args if args else message

    def get_status_text(self) -> str:
        return self.status_msg

    def get_message_text(self) -> str:
        return self.message

    def start_search(self):
        self.search_mode = True
        self.search_query = ""
        self.search_results = []
        self.search_index = 0
        self.set_status_message("Search: ")

    def end_search(self):
        self.search_mode = False
        self.search_query = ""
        self.search_results = []
        self.search_index = 0
        self.set_status_message("")

    def perform_search(self, query: Optional[str] = None):
        if query is not None:
            self.search_query = query
        if not self.search_query:
            return
        self.search_results = []
        pattern = re.escape(self.search_query)
        for r, line in enumerate(self.buffer):
            for m in re.finditer(pattern, line):
                self.search_results.append((r, m.start()))
        if self.search_results:
            self.search_index = 0
            self.jump_to_search_result()
            self.set_status_message(
                "Search: %s (%d/%d)",
                self.search_query,
                self.search_index + 1,
                len(self.search_results),
            )
        else:
            self.set_status_message("Search: %s (not found)", self.search_query)

    def jump_to_search_result(self, index: Optional[int] = None):
        if not self.search_results:
            return
        if index is None:
            index = self.search_index
        r, c = self.search_results[index]
        self.cursor_row = r
        self.cursor_col = c
        self.ensure_cursor_visible()

    def find_next(self):
        if not self.search_results:
            return
        self.search_index = (self.search_index + 1) % len(self.search_results)
        self.jump_to_search_result()
        self.set_status_message(
            "Search: %s (%d/%d)",
            self.search_query,
            self.search_index + 1,
            len(self.search_results),
        )

    def find_previous(self):
        if not self.search_results:
            return
        self.search_index = (self.search_index - 1) % len(self.search_results)
        self.jump_to_search_result()
        self.set_status_message(
            "Search: %s (%d/%d)",
            self.search_query,
            self.search_index + 1,
            len(self.search_results),
        )

    def setup_key_bindings(self, stdscr):
        # Mapping of key codes to handler functions
        self.key_map = {
            curses.KEY_UP: self.move_up,
            curses.KEY_DOWN: self.move_down,
            curses.KEY_LEFT: self.move_left,
            curses.KEY_RIGHT: self.move_right,
            curses.KEY_NPAGE: self.page_down,
            curses.KEY_PPAGE: self.page_up,
            curses.KEY_BACKSPACE: self.backspace,
            127: self.backspace,  # Some terminals send 127 for backspace
            curses.KEY_DC: self.delete_char,
            curses.KEY_ENTER: self.insert_newline,
            10: self.insert_newline,  # Enter key
            9: self.insert_tab,
            27: self.escape_key,  # Escape
            ord('s'): self.save_file,
            ord('q'): self.quit,
            ord('/'): self.start_search,
            ord('n'): self.find_next,
            ord('N'): self.find_previous,
        }

    def get_content(self) -> str:
        return "\n".join(self.buffer)

    def run(self):
        curses.wrapper(self._curses_main)

    # ----------------- Internal helpers -----------------

    def _curses_main(self, stdscr):
        curses.curs_set(1)
        stdscr.keypad(True)
        self.setup_key_bindings(stdscr)
        self.main_loop(stdscr)

    def main_loop(self, stdscr):
        while True:
            stdscr.clear()
            self.draw_buffer(stdscr)
            self.draw_status(stdscr)
            stdscr.move(self.cursor_row - self.top_line, self.cursor_col)
            stdscr.refresh()
            key = stdscr.getch()
            if self.search_mode:
                if key in (10, 13):  # Enter
                    self.perform_search(self.search_query)
                    self.end_search()
                elif key in (27,):  # Escape
                    self.end_search()
                elif key in (curses.KEY_BACKSPACE, 127):
                    self.search_query = self.search_query[:-1]
                    self.set_status_message("Search: %s", self.search_query)
                else:
                    try:
                        ch = chr(key)
                        if ch.isprintable():
                            self.search_query += ch
                            self.set_status_message("Search: %s", self.search_query)
                    except ValueError:
                        pass
                continue
            handler = self.key_map.get(key, None)
            if handler:
                handler()
            else:
                # Insert printable character
                try:
                    ch = chr(key)
                    if ch.isprintable():
                        self.insert_char(ch)
                except ValueError:
                    pass

    def draw_buffer(self, stdscr):
        h, w = stdscr.getmaxyx()
        visible_lines = h - 1  # Reserve last line for status
        for idx in range(visible_lines):
            line_no = self.top_line + idx
            if line_no >= len(self.buffer):
                break
            line = self.buffer[line_no]
            try:
                stdscr.addstr(idx, 0, line[: w - 1])
            except curses.error:
                pass

    def draw_status(self, stdscr):
        h, w = stdscr.getmaxyx()
        status = self.get_status_text()
        try:
            stdscr.addstr(h - 1, 0, status.ljust(w - 1), curses.A_REVERSE)
        except curses.error:
            pass

    def ensure_cursor_visible(self):
        h, _ = curses.initscr().getmaxyx()
        visible_lines = h - 1
        if self.cursor_row < self.top_line:
            self.top_line = self.cursor_row
        elif self.cursor_row >= self.top_line + visible_lines:
            self.top_line = self.cursor_row - visible_lines + 1

    # ----------------- Cursor movement -----------------

    def move_up(self):
        if self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_col = min(self.cursor_col, len(self.buffer[self.cursor_row]))
            self.ensure_cursor_visible()

    def move_down(self):
        if self.cursor_row < len(self.buffer) - 1:
            self.cursor_row += 1
            self.cursor_col = min(self.cursor_col, len(self.buffer[self.cursor_row]))
            self.ensure_cursor_visible()

    def move_left(self):
        if self.cursor_col > 0:
            self.cursor_col -= 1
        elif self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_col = len(self.buffer[self.cursor_row])
            self.ensure_cursor_visible()

    def move_right(self):
        line_len = len(self.buffer[self.cursor_row])
        if self.cursor_col < line_len:
            self.cursor_col += 1
        elif self.cursor_row < len(self.buffer) - 1:
            self.cursor_row += 1
            self.cursor_col = 0
            self.ensure_cursor_visible()

    def page_up(self):
        h, _ = curses.initscr().getmaxyx()
        visible_lines = h - 1
        self.cursor_row = max(0, self.cursor_row - visible_lines)
        self.cursor_col = min(self.cursor_col, len(self.buffer[self.cursor_row]))
        self.ensure_cursor_visible()

    def page_down(self):
        h, _ = curses.initscr().getmaxyx()
        visible_lines = h - 1
        self.cursor_row = min(len(self.buffer) - 1, self.cursor_row + visible_lines)
        self.cursor_col = min(self.cursor_col, len(self.buffer[self.cursor_row]))
        self.ensure_cursor_visible()

    # ----------------- Editing operations -----------------

    def insert_char(self, ch: str):
        line = self.buffer[self.cursor_row]
        self.buffer[self.cursor_row] = line[: self.cursor_col] + ch + line[self.cursor_col :]
        self.cursor_col += 1

    def insert_tab(self):
        self.insert_char("    ")

    def insert_newline(self):
        line = self.buffer[self.cursor_row]
        new_line = line[self.cursor_col :]
        self.buffer[self.cursor_row] = line[: self.cursor_col]
        self.buffer.insert(self.cursor_row + 1, new_line)
        self.cursor_row += 1
        self.cursor_col = 0
        self.ensure_cursor_visible()

    def backspace(self):
        if self.cursor_col > 0:
            line = self.buffer[self.cursor_row]
            self.buffer[self.cursor_row] = line[: self.cursor_col - 1] + line[self.cursor_col :]
            self.cursor_col -= 1
        elif self.cursor_row > 0:
            prev_line_len = len(self.buffer[self.cursor_row - 1])
            self.buffer[self.cursor_row - 1] += self.buffer[self.cursor_row]
            del self.buffer[self.cursor_row]
            self.cursor_row -= 1
            self.cursor_col = prev_line_len
            self.ensure_cursor_visible()

    def delete_char(self):
        line = self.buffer[self.cursor_row]
        if self.cursor_col < len(line):
            self.buffer[self.cursor_row] = line[: self.cursor_col] + line[self.cursor_col + 1 :]
        elif self.cursor_row < len(self.buffer) - 1:
            self.buffer[self.cursor_row] += self.buffer[self.cursor_row + 1]
            del self.buffer[self.cursor_row + 1]

    def escape_key(self):
        if self.search_mode:
            self.end_search()

    def quit(self):
        sys.exit(0)