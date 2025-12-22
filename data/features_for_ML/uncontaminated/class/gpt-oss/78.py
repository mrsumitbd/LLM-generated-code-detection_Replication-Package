import os
import shutil
import zipfile
import pathlib
import datetime
import sqlite3
import xml.etree.ElementTree as ET

class EPUBFixer:
    def __init__(self, manually_triggered: bool = False, current_position: str = None):
        self.manually_triggered = manually_triggered
        self.current_position = current_position
        self.original_epub_path = None
        self.files = {}  # mapping of file path to bytes
        self.issues = []  # list of issue strings

    def backup_original_file(self, epub_path):
        """Create a backup copy of the original EPUB."""
        self.original_epub_path = pathlib.Path(epub_path)
        backup_path = self.original_epub_path.with_suffix('.bak')
        shutil.copy2(self.original_epub_path, backup_path)

    def read_epub(self, epub_path):
        """Load all files from the EPUB into memory."""
        self.files = {}
        with zipfile.ZipFile(epub_path, 'r') as z:
            for info in z.infolist():
                if not info.is_dir():
                    self.files[info.filename] = z.read(info.filename)

    def _decode_text(self, data, filename):
        """Attempt to decode bytes to UTF-8, fallback to Latin-1."""
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = data.decode('latin-1')
                self.issues.append(f"Re-encoded {filename} from latin-1 to utf-8")
            except UnicodeDecodeError:
                self.issues.append(f"Failed to decode {filename}")
                text = data.decode('utf-8', errors='ignore')
        return text

    def fix_encoding(self):
        """Ensure all text files are UTF-8 encoded."""
        text_exts = {'.html', '.xhtml', '.xml', '.css', '.js'}
        for path, data in list(self.files.items()):
            if pathlib.Path(path).suffix.lower() in text_exts:
                text = self._decode_text(data, path)
                self.files[path] = text.encode('utf-8')

    def fix_body_id_link(self):
        """Add id='body' to <body> tags if missing."""
        for path, data in list(self.files.items()):
            if pathlib.Path(path).suffix.lower() in {'.html', '.xhtml'}:
                try:
                    root = ET.fromstring(data)
                except ET.ParseError:
                    self.issues.append(f"XML parse error in {path}")
                    continue
                body = root.find('.//body')
                if body is not None and 'id' not in body.attrib:
                    body.set('id', 'body')
                    self.issues.append(f"Added id='body' to <body> in {path}")
                    new_data = ET.tostring(root, encoding='utf-8')
                    self.files[path] = new_data

    def fix_book_language(self, default_language='en'):
        """Set lang attribute on <html> tags if missing."""
        for path, data in list(self.files.items()):
            if pathlib.Path(path).suffix.lower() in {'.html', '.xhtml'}:
                try:
                    root = ET.fromstring(data)
                except ET.ParseError:
                    self.issues.append(f"XML parse error in {path}")
                    continue
                html = root.find('.//html')
                if html is not None and 'lang' not in html.attrib:
                    html.set('lang', default_language)
                    self.issues.append(f"Set lang='{default_language}' on <html> in {path}")
                    new_data = ET.tostring(root, encoding='utf-8')
                    self.files[path] = new_data

    def fix_stray_img(self):
        """Remove <img> tags that reference missing files."""
        for path, data in list(self.files.items()):
            if pathlib.Path(path).suffix.lower() in {'.html', '.xhtml'}:
                try:
                    root = ET.fromstring(data)
                except ET.ParseError:
                    self.issues.append(f"XML parse error in {path}")
                    continue
                removed = False
                for img in root.findall('.//img'):
                    src = img.attrib.get('src')
                    if src and src not in self.files:
                        parent = img.getparent() if hasattr(img, 'getparent') else None
                        if parent is not None:
                            parent.remove(img)
                        else:
                            # fallback: remove by iterating children
                            for child in list(root):
                                if child is img:
                                    root.remove(child)
                        removed = True
                        self.issues.append(f"Removed stray <img> with src='{src}' in {path}")
                if removed:
                    new_data = ET.tostring(root, encoding='utf-8')
                    self.files[path] = new_data

    def write_epub(self, output_path):
        """Write the modified files to a new EPUB."""
        output_path = pathlib.Path(output_path)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for path, data in self.files.items():
                z.writestr(path, data)

    def export_issue_summary(self, epub_path):
        """Export a text file summarizing the issues found."""
        summary_path = pathlib.Path(epub_path).with_suffix('.issues.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"Issue summary for {epub_path}\n")
            f.write(f"Generated on {datetime.datetime.now().isoformat()}\n\n")
            for issue in self.issues:
                f.write(f"- {issue}\n")

    def add_entry_to_db(self, input_path, output_path):
        """Add a record to a SQLite database."""
        db_path = pathlib.Path('epub_fixer.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS fixes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_path TEXT,
                output_path TEXT,
                timestamp TEXT,
                issues TEXT
            )
        ''')
        cur.execute('''
            INSERT INTO fixes (input_path, output_path, timestamp, issues)
            VALUES (?, ?, ?, ?)
        ''', (
            input_path,
            output_path,
            datetime.datetime.now().isoformat(),
            '; '.join(self.issues)
        ))
        conn.commit()
        conn.close()

    def process(self, input_path, output_path=None, default_language='en'):
        """Full processing pipeline."""
        input_path = pathlib.Path(input_path)
        if output_path is None:
            output_path = input_path.with_name(input_path.stem + '_fixed.epub')
        else:
            output_path = pathlib.Path(output_path)

        self.backup_original_file(input_path)
        self.read_epub(input_path)
        self.fix_encoding()
        self.fix_body_id_link()
        self.fix_book_language(default_language)
        self.fix_stray_img()
        self.write_epub(output_path)
        self.export_issue_summary(output_path)
        self.add_entry_to_db(str(input_path), str(output_path))
        return output_path