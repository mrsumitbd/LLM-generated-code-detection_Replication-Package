import os
import zipfile
from xml.dom import minidom
import re
from pathlib import Path
import shutil
from acw_db import ACW_DB

class EPUBFixer:
    def __init__(self, manually_triggered:bool=False, current_position:str=None):
        self.manually_triggered = manually_triggered
        self.current_position = current_position # string in the form of "n/n"

        self.db = ACW_DB()
        self.acw_settings = self.db.acw_settings

        self.fixed_problems = []
        self.files = {}
        self.binary_files = {}
        self.entries = []


    def backup_original_file(self, epub_path):
        """Backup original file"""
        if self.acw_settings['auto_backup_epub_fixes']:
            try:
                output_path = os.path.join(os.environ.get("ACW_CONFIG_DIR", "/config"), "processed_books", "fixed_originals")
                shutil.copy2(epub_path, output_path)
            except Exception as e:
                print_and_log(f"[acw-kindle-epub-fixer] ERROR - Error occurred when backing up {epub_path} to {output_path}:\n{e}", log=self.manually_triggered)

    def read_epub(self, epub_path):
        """Read EPUB file contents"""
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            self.entries = zip_ref.namelist()
            for filename in self.entries:
                ext = filename.split('.')[-1]
                if filename == 'mimetype' or ext in ['html', 'xhtml', 'htm', 'xml', 'svg', 'css', 'opf', 'ncx']:
                    self.files[filename] = zip_ref.read(filename).decode('utf-8')
                else:
                    self.binary_files[filename] = zip_ref.read(filename)

    def fix_encoding(self):
        """Add UTF-8 encoding declaration if missing"""
        encoding = '<?xml version="1.0" encoding="utf-8"?>'
        regex = r'^<\?xml\s+version=["\'][\d.]+["\']\s+encoding=["\'][a-zA-Z\d\-\.]+["\'].*?\?>'

        for filename in list(self.files.keys()):
            ext = filename.split('.')[-1]
            if ext in ['html', 'xhtml']:
                html = self.files[filename]
                html = html.lstrip()
                if not re.match(regex, html, re.IGNORECASE):
                    html = encoding + '\n' + html
                    self.fixed_problems.append(f"Fixed encoding for file {filename}")
                self.files[filename] = html

    def fix_body_id_link(self):
        """Fix linking to body ID showing up as unresolved hyperlink"""
        body_id_list = []

        # Create list of ID tag of <body>
        for filename in self.files:
            ext = filename.split('.')[-1]
            if ext in ['html', 'xhtml']:
                html = self.files[filename]
                dom = minidom.parseString(html)
                body_elements = dom.getElementsByTagName('body')
                if body_elements and body_elements[0].hasAttribute('id'):
                    body_id = body_elements[0].getAttribute('id')
                    if body_id:
                        link_target = os.path.basename(filename) + '#' + body_id
                        body_id_list.append([link_target, os.path.basename(filename)])

        # Replace all
        for filename in self.files:
            for src, target in body_id_list:
                if src in self.files[filename]:
                    self.files[filename] = self.files[filename].replace(src, target)
                    self.fixed_problems.append(f"Replaced link target {src} with {target} in file {filename}.")

    def fix_book_language(self, default_language='en'):
        """Fix language field not defined or not available"""
        # From https://kdp.amazon.com/en_US/help/topic/G200673300
        allowed_languages = [
            # ISO 639-1
            'af', 'gsw', 'ar', 'eu', 'nb', 'br', 'ca', 'zh', 'kw', 'co', 'da', 'nl', 'stq', 'en', 'fi', 'fr', 'fy', 'gl',
            'de', 'gu', 'hi', 'is', 'ga', 'it', 'ja', 'lb', 'mr', 'ml', 'gv', 'frr', 'nb', 'nn', 'pl', 'pt', 'oc', 'rm',
            'sco', 'gd', 'es', 'sv', 'ta', 'cy',
            # ISO 639-2
            'afr', 'ara', 'eus', 'baq', 'nob', 'bre', 'cat', 'zho', 'chi', 'cor', 'cos', 'dan', 'nld', 'dut', 'eng', 'fin',
            'fra', 'fre', 'fry', 'glg', 'deu', 'ger', 'guj', 'hin', 'isl', 'ice', 'gle', 'ita', 'jpn', 'ltz', 'mar', 'mal',
            'glv', 'nor', 'nno', 'por', 'oci', 'roh', 'gla', 'spa', 'swe', 'tam', 'cym', 'wel',
        ]

        # Find OPF file
        if 'META-INF/container.xml' not in self.files:
            print('Cannot find META-INF/container.xml')
            return

        container_xml = minidom.parseString(self.files['META-INF/container.xml'])
        opf_filename = None
        for rootfile in container_xml.getElementsByTagName('rootfile'):
            if rootfile.getAttribute('media-type') == 'application/oebps-package+xml':
                opf_filename = rootfile.getAttribute('full-path')
                break

        # Read OPF file
        if not opf_filename or opf_filename not in self.files:
            print('Cannot find OPF file!')
            return

        try:
            opf = minidom.parseString(self.files[opf_filename])
            language_tags = opf.getElementsByTagName('dc:language')
            language = default_language
            original_language = 'undefined'

            if not language_tags:
                # Use default language if no language tag exists
                self.fixed_problems.append(f"No language tag found. Setting to default: {default_language}")
            else:
                language = language_tags[0].firstChild.nodeValue
                original_language = language

            simplified_lang = language.split('-')[0].lower()
            if simplified_lang not in allowed_languages:
                # If language is not supported, use default
                language = default_language
                self.fixed_problems.append(f"Unsupported language {original_language}. Changed to {default_language}")

            if not language_tags:
                language_tag = opf.createElement('dc:language')
                text_node = opf.createTextNode(language)
                language_tag.appendChild(text_node)
                metadata = opf.getElementsByTagName('metadata')[0]
                metadata.appendChild(language_tag)
            else:
                language_tags[0].firstChild.nodeValue = language

            if language != original_language:
                self.files[opf_filename] = opf.toxml()
                self.fixed_problems.append(f"Changed document language from {original_language} to {language}")

        except Exception as e:
            print(f'Error trying to parse OPF file as XML: {e}')

    def fix_stray_img(self):
        """Fix stray IMG tags"""
        for filename in list(self.files.keys()):
            ext = filename.split('.')[-1]
            if ext in ['html', 'xhtml']:
                dom = minidom.parseString(self.files[filename])
                stray_img = []
                
                for img in dom.getElementsByTagName('img'):
                    if not img.getAttribute('src'):
                        stray_img.append(img)

                if stray_img:
                    for img in stray_img:
                        img.parentNode.removeChild(img)
                    self.fixed_problems.append(f"Remove stray image tag(s) in {filename}")
                    self.files[filename] = dom.toxml()

    def write_epub(self, output_path):
        """Write EPUB file"""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            # First write mimetype file
            if 'mimetype' in self.files:
                zip_ref.writestr('mimetype', self.files['mimetype'], compress_type=zipfile.ZIP_STORED)

            # Add text files
            for filename, content in self.files.items():
                if filename != 'mimetype':
                    zip_ref.writestr(filename, content)

            # Add binary files
            for filename, content in self.binary_files.items():
                zip_ref.writestr(filename, content)

    def export_issue_summary(self, epub_path):
        if self.current_position:
            line_suffix = f"[acw-kindle-epub-fixer] {self.current_position} - "
        else:
            line_suffix = "[acw-kindle-epub-fixer] "
        
        if self.fixed_problems:
            print_and_log(line_suffix + f"{len(self.fixed_problems)} issues fixed with {epub_path}:", log=self.manually_triggered)
            for count, problem in enumerate(self.fixed_problems):
                print_and_log(f"   {str(count + 1).zfill(2)} - {problem}", log=self.manually_triggered)            
        else:
            print_and_log(line_suffix + f"No issues found! - {epub_path}", log=self.manually_triggered)

    def add_entry_to_db(self, input_path, output_path):
        if self.fixed_problems:
            fixed_problems = []
            for count, problem in enumerate(self.fixed_problems):
                fixed_problems.append(f"{str(count + 1).zfill(2)} - {problem}")
            fixed_problems = "\n".join(fixed_problems)
        else:
            fixed_problems = "No fixes required"

        self.db.epub_fixer_add_entry(Path(input_path).stem,
                                    bool(self.manually_triggered),
                                    len(self.fixed_problems),
                                    str(self.acw_settings['auto_backup_epub_fixes']),
                                    output_path,
                                    fixed_problems)


    def process(self, input_path, output_path=None, default_language='en'):
        """Process a single EPUB file"""
        if not output_path:
            output_path = input_path

        # Back Up Original File
        print_and_log("[acw-kindle-epub-fixer] Backing up original file...", log=self.manually_triggered)
        self.backup_original_file(input_path)

        # Load EPUB
        print_and_log("[acw-kindle-epub-fixer] Loading provided EPUB...", log=self.manually_triggered)
        self.read_epub(input_path)

        # Run fixing procedures
        print_and_log("[acw-kindle-epub-fixer] Checking linking to body ID to prevent unresolved hyperlinks...", log=self.manually_triggered)
        self.fix_body_id_link()
        print_and_log("[acw-kindle-epub-fixer] Checking language field tag is valid...", log=self.manually_triggered)
        self.fix_book_language(default_language)
        print_and_log("[acw-kindle-epub-fixer] Checking for stray images...", log=self.manually_triggered)
        self.fix_stray_img()
        print_and_log("[acw-kindle-epub-fixer] Checking UTF-8 encoding declaration...", log=self.manually_triggered)
        self.fix_encoding()

        # Notify user and/or write to log
        self.export_issue_summary(input_path)

        # Write EPUB
        print_and_log("[acw-kindle-epub-fixer] Writing EPUB...", log=self.manually_triggered)
        if Path(output_path).is_dir():
            output_path = output_path + os.path.basename(input_path)
        self.write_epub(output_path)
        print_and_log("[acw-kindle-epub-fixer] EPUB successfully written.", log=self.manually_triggered)
        
        # Add entry to acw.db
        print_and_log("[acw-kindle-epub-fixer] Adding run to acw.db...", log=self.manually_triggered)
        self.add_entry_to_db(input_path, output_path)
        print_and_log("[acw-kindle-epub-fixer] Run successfully added to acw.db.", log=self.manually_triggered)
        return self.fixed_problems