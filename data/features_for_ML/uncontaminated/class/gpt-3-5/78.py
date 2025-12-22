import os
import shutil
from ebooklib import epub
from bs4 import BeautifulSoup

class EPUBFixer:

    def __init__(self, manually_triggered: bool = False, current_position: str = None):
        self.manually_triggered = manually_triggered
        self.current_position = current_position
        self.original_epub = None
        self.fixed_epub = None

    def backup_original_file(self, epub_path):
        shutil.copy(epub_path, epub_path + '.bak')

    def read_epub(self, epub_path):
        self.original_epub = epub.read_epub(epub_path)

    def fix_encoding(self):
        for item in self.original_epub.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8', 'ignore')
                item.set_content(content.encode('utf-8'))

    def fix_body_id_link(self):
        for item in self.original_epub.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                for tag in soup.find_all():
                    if 'id' in tag.attrs:
                        tag['id'] = tag['id'].replace(' ', '_')
                item.set_content(str(soup))

    def fix_book_language(self, default_language='en'):
        self.original_epub.set_language(default_language)

    def fix_stray_img(self):
        for item in self.original_epub.get_items():
            if item.get_type() == ebooklib.ITEM_IMAGE:
                self.original_epub.delete_item(item)

    def write_epub(self, output_path):
        epub.write_epub(output_path, self.original_epub)

    def export_issue_summary(self, epub_path):
        summary = f"EPUBFixer Summary for {epub_path}:\n"
        summary += f"Manually Triggered: {self.manually_triggered}\n"
        summary += f"Current Position: {self.current_position}\n"
        return summary

    def add_entry_to_db(self, input_path, output_path):
        # Add entry to database with input_path and output_path
        pass

    def process(self, input_path, output_path=None, default_language='en'):
        self.read_epub(input_path)
        self.backup_original_file(input_path)
        self.fix_encoding()
        self.fix_body_id_link()
        self.fix_book_language(default_language)
        self.fix_stray_img()
        if output_path:
            self.write_epub(output_path)
        else:
            self.write_epub(input_path)