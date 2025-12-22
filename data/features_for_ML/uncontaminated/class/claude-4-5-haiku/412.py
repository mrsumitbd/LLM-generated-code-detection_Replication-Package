class RobotFrameworkDocStorage:
    """Storage and retrieval of Robot Framework library documentation using native libdoc."""

    def __init__(self):
        self.libraries = {}
        self.keywords = {}
        self._initialize_libraries()

    def _initialize_libraries(self):
        """Initialize standard Robot Framework libraries."""
        standard_libs = [
            'BuiltIn',
            'Collections',
            'DateTime',
            'Dialogs',
            'Easter',
            'Enum',
            'FileSystem',
            'FTP',
            'HTTP',
            'JSON',
            'Logging',
            'Process',
            'Reserved',
            'Screenshot',
            'String',
            'Telnet',
            'XML',
        ]
        
        for lib_name in standard_libs:
            self._load_library_documentation(lib_name)

    def _load_library_documentation(self, library_name: str) -> bool:
        """Load library documentation using libdoc."""
        try:
            from robot.libdocpkg import LibraryDocumentation
            
            lib_doc = LibraryDocumentation(library_name)
            
            lib_info = RFLibraryInfo(
                name=lib_doc.name,
                doc=lib_doc.doc,
                version=lib_doc.version,
                type=lib_doc.type,
                scope=getattr(lib_doc, 'scope', 'GLOBAL'),
                named_args=getattr(lib_doc, 'named_args', False),
                keywords=[]
            )
            
            for kw_doc in lib_doc.keywords:
                kw_info = self._extract_keyword_from_libdoc(library_name, kw_doc)
                lib_info.keywords.append(kw_info)
                
                normalized_name = self._normalize_name(kw_info.name)
                if normalized_name not in self.keywords:
                    self.keywords[normalized_name] = []
                self.keywords[normalized_name].append(kw_info)
            
            self.libraries[library_name] = lib_info
            return True
        except Exception:
            return False

    def _extract_keyword_from_libdoc(self, library_name: str, kw_doc: 'KeywordDoc') -> 'RFKeywordInfo':
        """Extract keyword information from libdoc KeywordDoc."""
        args = []
        if hasattr(kw_doc, 'args'):
            args = list(kw_doc.args)
        
        short_doc = self._create_short_doc(kw_doc.doc if kw_doc.doc else '')
        
        return RFKeywordInfo(
            name=kw_doc.name,
            library=library_name,
            doc=kw_doc.doc if kw_doc.doc else '',
            short_doc=short_doc,
            args=args,
            tags=list(kw_doc.tags) if hasattr(kw_doc, 'tags') else []
        )

    def _create_short_doc(self, doc: str, max_length: int = 120) -> str:
        """Create a short documentation string."""
        if not doc:
            return ''
        
        lines = doc.split('\n')
        first_line = lines[0].strip()
        
        if len(first_line) <= max_length:
            return first_line
        
        return first_line[:max_length].rsplit(' ', 1)[0] + '...'

    def find_keyword(self, keyword_name: str) -> 'Optional[RFKeywordInfo]':
        """Find a keyword by name."""
        normalized_name = self._normalize_name(keyword_name)
        
        if normalized_name in self.keywords:
            keywords = self.keywords[normalized_name]
            if keywords:
                return keywords[0]
        
        return None

    def get_keywords_by_library(self, library_name: str) -> 'List[RFKeywordInfo]':
        """Get all keywords from a specific library."""
        if library_name in self.libraries:
            return self.libraries[library_name].keywords
        return []

    def get_all_keywords(self) -> 'List[RFKeywordInfo]':
        """Get all keywords from all loaded libraries."""
        all_keywords = []
        for lib_info in self.libraries.values():
            all_keywords.extend(lib_info.keywords)
        return all_keywords

    def get_keywords_from_libraries(self, library_names: 'List[str]') -> 'List[RFKeywordInfo]':
        """Get keywords from specified libraries."""
        keywords = []
        for lib_name in library_names:
            keywords.extend(self.get_keywords_by_library(lib_name))
        return keywords

    def search_keywords(self, pattern: str) -> 'List[RFKeywordInfo]':
        """Search keywords by pattern."""
        import re
        
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            regex = re.compile(re.escape(pattern), re.IGNORECASE)
        
        results = []
        for keyword in self.get_all_keywords():
            if regex.search(keyword.name) or regex.search(keyword.doc):
                results.append(keyword)
        
        return results

    def get_library_documentation(self, library_name: str) -> 'Optional[RFLibraryInfo]':
        """Get documentation for a library."""
        return self.libraries.get(library_name)

    def get_keyword_documentation(self, keyword_name: str, library_name: str = None) -> 'Optional[RFKeywordInfo]':
        """Get documentation for a keyword."""
        if library_name:
            keywords = self.get_keywords_by_library(library_name)
            normalized_kw = self._normalize_name(keyword_name)
            for kw in keywords:
                if self._normalize_name(kw.name) == normalized_kw:
                    return kw
            return None
        
        return self.find_keyword(keyword_name)

    def get_keywords_documentation_all(self, keyword_name: str) -> 'List[RFKeywordInfo]':
        """Get documentation for a keyword from all libraries."""
        normalized_name = self._normalize_name(keyword_name)
        return self.keywords.get(normalized_name, [])

    def _normalize_name(self, name: str) -> str:
        """Normalize a name for comparison."""
        return name.lower().replace(' ', '').replace('_', '')

    def _extract_hybrid_signature(self, keyword_name: str, library_name: str) -> 'Optional[List[str]]':
        """Extract signature from hybrid keyword."""
        try:
            import inspect
            from robot.running.librarykeyword import LibraryKeyword
            
            if library_name not in self.libraries:
                return None
            
            lib_module = __import__(library_name)
            if hasattr(lib_module, keyword_name):
                keyword_obj = getattr(lib_module, keyword_name)
                if isinstance(keyword_obj, LibraryKeyword):
                    return self._extract_from_argumentspec(inspect.getfullargspec(keyword_obj.method))
        except Exception:
            pass
        
        return None

    def _is_decorated_keyword(self, args_spec) -> bool:
        """Check if keyword is decorated."""
        return hasattr(args_spec, 'keywords') or hasattr(args_spec, 'varkw')

    def _extract_from_argumentspec(self, args_spec) -> 'List[str]':
        """Extract arguments from ArgumentSpec."""
        args = []
        
        if hasattr(args_spec, 'args') and args_spec.args:
            args.extend(args_spec.args)
        
        if hasattr(args_spec, 'varargs') and args_spec.varargs:
            args.append(f'*{args_spec.varargs}')
        
        if hasattr(args_spec, 'varkw') and args_spec.varkw:
            args.append(f'**{args_spec.varkw}')
        
        return args

    def _extract_from_closure(self, keyword_obj, keyword_name: str, library_name: str) -> 'Optional[List[str]]':
        """Extract arguments from keyword closure."""
        try:
            if hasattr(keyword_obj, '__closure__') and keyword_obj.__closure__:
                for cell in keyword_obj.__closure__:
                    if hasattr(cell.cell_contents, '__name__'):
                        if cell.cell_contents.__name__ == keyword_name:
                            import inspect
                            return self._extract_from_argumentspec(inspect.getfullargspec(cell.cell_contents))
        except Exception:
            pass
        
        return None

    def refresh_library(self, library_name: str) -> bool:
        """Refresh library documentation."""
        if library_name in self.libraries:
            del self.libraries[library_name]
            
            for kw_list in self.keywords.values():
                kw_list[:] = [kw for kw in kw_list if kw.library != library_name]
        
        return self._load_library_documentation(library_name)

    def ensure_library_loaded(self, library_name: str) -> bool:
        """Ensure a library is loaded."""
        if library_name not in self.libraries:
            return self._load_library_documentation(library_name)
        return True

    def get_library_status(self) -> 'Dict[str, Any]':
        """Get status of all loaded libraries."""
        status = {}
        for lib_name, lib_info in self.libraries.items():
            status[lib_name] = {
                'name': lib_info.name,
                'version': lib_info.version,
                'type': lib_info.type,
                'keywords_count': len(lib_info.keywords)
            }
        return status

    def is_available(self) -> bool:
        """Check if Robot Framework is available."""
        try:
            import robot
            return True
        except ImportError:
            return False


class RFKeywordInfo:
    """Information about a Robot Framework keyword."""
    
    def __init__(self, name: str, library: str, doc: str, short_doc: str, args: 'List[str]', tags: 'List[str]'):
        self.name = name
        self.library = library
        self.doc = doc
        self.short_doc = short_doc
        self.args = args
        self.tags = tags


class RFLibraryInfo:
    """Information about a Robot Framework library."""
    
    def __init__(self, name: str, doc: str, version: str, type: str, scope: str, named_args: bool, keywords: 'List[RFKeywordInfo]'):
        self.name = name
        self.doc = doc
        self.version = version
        self.type = type
        self.scope = scope
        self.named_args = named_args
        self.keywords = keywords