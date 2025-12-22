import os
import re
from typing import List, Optional, Dict, Any
from robot.libdocpkg.model import KeywordDoc, LibraryDoc
from robot.libraries.BuiltIn import BuiltIn

class RFKeywordInfo:
    def __init__(self, library_name: str, keyword_name: str, short_doc: str, full_doc: str, args: List[str]):
        self.library_name = library_name
        self.keyword_name = keyword_name
        self.short_doc = short_doc
        self.full_doc = full_doc
        self.args = args

class RFLibraryInfo:
    def __init__(self, library_name: str, version: str, doc: str, keywords: List[RFKeywordInfo]):
        self.library_name = library_name
        self.version = version
        self.doc = doc
        self.keywords = keywords

class RobotFrameworkDocStorage:
    """Storage and retrieval of Robot Framework library documentation using native libdoc."""

    def __init__(self):
        self._libraries = {}

    def _initialize_libraries(self):
        builtin = BuiltIn()
        for library_name in builtin.get_library_names():
            self._load_library_documentation(library_name)

    def _load_library_documentation(self, library_name: str) -> bool:
        try:
            libdoc = BuiltIn().get_library_instance('libdoc').get_keyword_documentation(library_name)
            self._libraries[library_name] = self._extract_library_info(libdoc)
            return True
        except Exception:
            return False

    def _extract_library_info(self, libdoc: LibraryDoc) -> RFLibraryInfo:
        keywords = [self._extract_keyword_from_libdoc(libdoc.name, kw) for kw in libdoc.keywords]
        return RFLibraryInfo(libdoc.name, libdoc.version, libdoc.doc, keywords)

    def _extract_keyword_from_libdoc(self, library_name: str, kw_doc: KeywordDoc) -> RFKeywordInfo:
        short_doc = self._create_short_doc(kw_doc.doc)
        args = self._extract_hybrid_signature(kw_doc.name, library_name) or self._extract_from_argumentspec(kw_doc.args)
        return RFKeywordInfo(library_name, kw_doc.name, short_doc, kw_doc.doc, args)

    def _create_short_doc(self, doc: str, max_length: int = 120) -> str:
        return (doc.split('\n')[0] + '...') if len(doc) > max_length else doc

    def find_keyword(self, keyword_name: str) -> Optional[RFKeywordInfo]:
        for library_name, library_info in self._libraries.items():
            for keyword in library_info.keywords:
                if self._normalize_name(keyword.keyword_name) == self._normalize_name(keyword_name):
                    return keyword
        return None

    def get_keywords_by_library(self, library_name: str) -> List[RFKeywordInfo]:
        if library_name in self._libraries:
            return self._libraries[library_name].keywords
        return []

    def get_all_keywords(self) -> List[RFKeywordInfo]:
        keywords = []
        for library_info in self._libraries.values():
            keywords.extend(library_info.keywords)
        return keywords

    def get_keywords_from_libraries(self, library_names: List[str]) -> List[RFKeywordInfo]:
        keywords = []
        for library_name in library_names:
            keywords.extend(self.get_keywords_by_library(library_name))
        return keywords

    def search_keywords(self, pattern: str) -> List[RFKeywordInfo]:
        keywords = self.get_all_keywords()
        return [kw for kw in keywords if pattern.lower() in self._normalize_name(kw.keyword_name).lower()]

    def get_library_documentation(self, library_name: str) -> Optional[RFLibraryInfo]:
        if library_name in self._libraries:
            return self._libraries[library_name]
        return None

    def get_keyword_documentation(self, keyword_name: str, library_name: str = None) -> Optional[RFKeywordInfo]:
        if library_name:
            return self.find_keyword(keyword_name)
        for library_info in self._libraries.values():
            for keyword in library_info.keywords:
                if self._normalize_name(keyword.keyword_name) == self._normalize_name(keyword_name):
                    return keyword
        return None

    def get_keywords_documentation_all(self, keyword_name: str) -> List[RFKeywordInfo]:
        return [kw for kw in self.get_all_keywords() if self._normalize_name(kw.keyword_name) == self._normalize_name(keyword_name)]

    def _normalize_name(self, name: str) -> str:
        return re.sub(r'\s+', ' ', name.strip().lower())

    def _extract_hybrid_signature(self, keyword_name: str, library_name: str) -> Optional[List[str]]:
        try:
            keyword_obj = BuiltIn().get_keyword_instance(f'{library_name}.{keyword_name}')
            if self._is_decorated_keyword(keyword_obj.arguments):
                return self._extract_from_closure(keyword_obj, keyword_name, library_name)
        except Exception:
            pass
        return None

    def _is_decorated_keyword(self, args_spec) -> bool:
        return isinstance(args_spec, list) and len(args_spec) > 0 and isinstance(args_spec[0], str)

    def _extract_from_argumentspec(self, args_spec) -> List[str]:
        return [arg.replace('$', '') for arg in args_spec]

    def _extract_from_closure(self, keyword_obj, keyword_name: str, library_name: str) -> Optional[List[str]]:
        try:
            return self._extract_from_argumentspec(keyword_obj.arguments)
        except Exception:
            return None

    def refresh_library(self, library_name: str) -> bool:
        return self._load_library_documentation(library_name)

    def ensure_library_loaded(self, library_name: str) -> bool:
        if library_name not in self._libraries:
            return self._load_library_documentation(library_name)
        return True

    def get_library_status(self) -> Dict[str, Any]:
        return {
            'loaded_libraries': list(self._libraries.keys()),
            'total_keywords': sum(len(lib.keywords) for lib in self._libraries.values())
        }

    def is_available(self) -> bool:
        return len(self._libraries) > 0