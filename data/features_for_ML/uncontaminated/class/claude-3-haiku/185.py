class ExternalImportResolver:
    def __init__(self, import_paths: list[str]):
        self.import_paths = import_paths

    def resolve(self, imp: Import) -> str | None:
        for path in self.import_paths:
            try:
                module_path = os.path.join(path, *imp.parts) + ".py"
                if os.path.exists(module_path):
                    return module_path
            except (OSError, IOError):
                continue
        return None