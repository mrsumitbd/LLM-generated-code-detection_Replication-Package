import os
import shutil
import re
from lxml import etree
from ebooklib import epub

class EPUBFixer:
    def __init__(self, manually_triggered: bool = False, current_position: str = None):
        self.manually_triggered = manually_triggered
        self.current_position = current_position
        self.book = None
        self.issues = []

    def backup_original_file(self, epub_path):
        backup_path = f"{epub_path}.bak"
        shutil.copy2(epub_path, backup_path)

    def read_epub(self, epub_path):
        self.book = epub.read_epub(epub_path)

    def fix_encoding(self):
        for item in self.book.get_items():
            if hasattr(item, 'content'):
                item.content = item.content.decode('utf-8', 'replace').encode('utf-8')

    def fix_body_id_link(self):
        for item in self.book.get_items_of_type(epub.ITEM_DOCUMENT):
            tree = etree.HTML(item.get_content())
            for link in tree.xpath('//a[@href]'):
                href = link.get('href')
                if href.startswith('#'):
                    link.set('href', f'#{href[1:]}')
            item.set_content(etree.tostring(tree, encoding='utf-8'))

    def fix_book_language(self, default_language='en'):
        self.book.set_language(self.book.get_language() or default_language)

    def fix_stray_img(self):
        for item in self.book.get_items_of_type(epub.ITEM_IMAGE):
            if item.get_name() not in [i.get_name() for i in self.book.get_items_of_type(epub.ITEM_DOCUMENT)]:
                self.book.add_item(item)

    def write_epub(self, output_path):
        epub.write_epub(output_path, self.book)

    def export_issue_summary(self, epub_path):
        with open(f"{os.path.splitext(epub_path)[0]}_issues.txt", 'w') as f:
            f.write('\n'.join(self.issues))

    def add_entry_to_db(self, input_path, output_path):
        pass

    def process(self, input_path, output_path=None, default_language='en'):
        self.backup_original_file(input_path)
        self.read_epub(input_path)
        self.fix_encoding()
        self.fix_body_id_link()
        self.fix_book_language(default_language)
        self.fix_stray_img()

        if output_path is None:
            output_path = input_path
        self.write_epub(output_path)
        self.export_issue_summary(output_path)
        self.add_entry_to_db(input_path, output_path)