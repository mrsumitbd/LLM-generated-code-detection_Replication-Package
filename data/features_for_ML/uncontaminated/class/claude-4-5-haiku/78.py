import os
import shutil
import zipfile
import tempfile
import sqlite3
from pathlib import Path
from lxml import etree
from datetime import datetime
import json

class EPUBFixer:

    def __init__(self, manually_triggered:bool=False, current_position:str=None):
        self.manually_triggered = manually_triggered
        self.current_position = current_position
        self.epub_path = None
        self.temp_dir = None
        self.content_files = {}
        self.issues = []
        self.metadata = {}

    def backup_original_file(self, epub_path):
        backup_path = epub_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(epub_path, backup_path)
        return backup_path

    def read_epub(self, epub_path):
        self.epub_path = epub_path
        self.temp_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        
        # Read OPF file to get content files
        opf_path = self._find_opf_file()
        if opf_path:
            self._parse_opf(opf_path)
        
        # Read all XHTML/HTML files
        self._read_content_files()

    def _find_opf_file(self):
        container_path = os.path.join(self.temp_dir, 'META-INF', 'container.xml')
        if os.path.exists(container_path):
            tree = etree.parse(container_path)
            root = tree.getroot()
            ns = {'container': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            rootfile = root.find('.//container:rootfile', ns)
            if rootfile is not None:
                return os.path.join(self.temp_dir, rootfile.get('full-path'))
        return None

    def _parse_opf(self, opf_path):
        tree = etree.parse(opf_path)
        root = tree.getroot()
        ns = {'opf': 'http://www.idpf.org/2007/opf'}
        
        # Extract metadata
        metadata = root.find('.//opf:metadata', ns)
        if metadata is not None:
            lang = metadata.find('.//dc:language', {'dc': 'http://purl.org/dc/elements/1.1/'})
            if lang is not None:
                self.metadata['language'] = lang.text

    def _read_content_files(self):
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.endswith(('.xhtml', '.html', '.htm')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.content_files[file_path] = f.read()
                    except:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            self.content_files[file_path] = f.read()

    def fix_encoding(self):
        for file_path, content in self.content_files.items():
            try:
                content.encode('utf-8')
            except UnicodeEncodeError:
                # Fix encoding issues
                fixed_content = content.encode('utf-8', errors='replace').decode('utf-8')
                self.content_files[file_path] = fixed_content
                self.issues.append(f"Fixed encoding in {os.path.basename(file_path)}")

    def fix_body_id_link(self):
        for file_path, content in self.content_files.items():
            try:
                parser = etree.HTMLParser()
                tree = etree.fromstring(content.encode('utf-8'), parser)
                
                # Check for body without id
                body = tree.find('.//body')
                if body is not None and body.get('id') is None:
                    body.set('id', 'body')
                    self.content_files[file_path] = etree.tostring(tree, encoding='unicode', method='html')
                    self.issues.append(f"Added id to body in {os.path.basename(file_path)}")
            except:
                pass

    def fix_book_language(self, default_language='en'):
        opf_path = self._find_opf_file()
        if opf_path and os.path.exists(opf_path):
            tree = etree.parse(opf_path)
            root = tree.getroot()
            ns = {'opf': 'http://www.idpf.org/2007/opf', 'dc': 'http://purl.org/dc/elements/1.1/'}
            
            metadata = root.find('.//opf:metadata', ns)
            if metadata is not None:
                lang = metadata.find('.//dc:language', ns)
                if lang is None:
                    lang = etree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}language')
                    lang.text = default_language
                    tree.write(opf_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
                    self.issues.append(f"Set book language to {default_language}")
                elif not lang.text:
                    lang.text = default_language
                    tree.write(opf_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
                    self.issues.append(f"Fixed empty language to {default_language}")

    def fix_stray_img(self):
        for file_path, content in self.content_files.items():
            try:
                parser = etree.HTMLParser()
                tree = etree.fromstring(content.encode('utf-8'), parser)
                
                # Find images without alt text
                images = tree.findall('.//img')
                fixed = False
                for img in images:
                    if img.get('alt') is None:
                        img.set('alt', 'Image')
                        fixed = True
                
                if fixed:
                    self.content_files[file_path] = etree.tostring(tree, encoding='unicode', method='html')
                    self.issues.append(f"Fixed stray images in {os.path.basename(file_path)}")
            except:
                pass

    def write_epub(self, output_path):
        if self.temp_dir is None:
            return
        
        # Write modified content files back
        for file_path, content in self.content_files.items():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create new EPUB
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname)
        
        # Cleanup
        shutil.rmtree(self.temp_dir)
        self.temp_dir = None

    def export_issue_summary(self, epub_path):
        summary = {
            'epub_file': os.path.basename(epub_path),
            'timestamp': datetime.now().isoformat(),
            'manually_triggered': self.manually_triggered,
            'issues_found': len(self.issues),
            'issues': self.issues
        }
        return summary

    def add_entry_to_db(self, input_path, output_path):
        db_path = os.path.join(os.path.dirname(input_path), 'epub_fixes.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS fixes
                         (id INTEGER PRIMARY KEY, input_path TEXT, output_path TEXT, 
                          timestamp TEXT, issues_count INTEGER, manually_triggered INTEGER)''')
        
        cursor.execute('''INSERT INTO fixes (input_path, output_path, timestamp, issues_count, manually_triggered)
                         VALUES (?, ?, ?, ?, ?)''',
                      (input_path, output_path, datetime.now().isoformat(), len(self.issues), self.manually_triggered))
        
        conn.commit()
        conn.close()

    def process(self, input_path, output_path=None, default_language='en'):
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_fixed{ext}"
        
        self.backup_original_file(input_path)
        self.read_epub(input_path)
        self.fix_encoding()
        self.fix_body_id_link()
        self.fix_book_language(default_language)
        self.fix_stray_img()
        self.write_epub(output_path)
        self.add_entry_to_db(input_path, output_path)
        
        return self.export_issue_summary(input_path)