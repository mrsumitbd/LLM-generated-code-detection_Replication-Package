from ausweiskopie.editor.importer import IMPORTERS, get_importer, import_from_field_definition
from ausweiskopie.ui.dialogs import openfilename

def _fn():
            importer = get_importer(import_type)
            if not importer:
                return

            infile = openfilename(
                filetypes=importer.supported_file_extensions,
                parent=self.winfo_toplevel(),
            )
            if not infile:
                return

            with open(infile, 'r', encoding='utf-8') as infile:
                file_content = infile.read()

            self.fields = importer.import_layout(file_content)
            self.root.update_status('EDITOR_STATUS_LOADED_LAYOUT', {'count': len(self.fields)})