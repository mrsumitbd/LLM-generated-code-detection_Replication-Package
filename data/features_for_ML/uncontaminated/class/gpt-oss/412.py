import os
import re
import fnmatch
from typing import List, Optional, Dict, Any
from robot.libdoc import Libdoc
from robot.libdoc import KeywordDoc
from dataclasses import dataclass, field


@dataclass
class RFKeywordInfo:
    name: str
    doc: str
    args: List[str] = field(default_factory=list)
    returns: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    library: Optional[str] = None


@dataclass
class RFLibraryInfo:
    name: str
    version: Optional[str] = None
    doc: Optional[str] = None
    keywords: List[RFKeywordInfo] = field(default_factory=list)


class RobotFrameworkDocStorage:
    """Storage and retrieval of Robot Framework library documentation using native libdoc."""

    def __init__(self):
        self._libraries: Dict[str, RFLibraryInfo] = {}
        self._initialize_libraries()

    def _initialize_libraries(self):
        """Initial load of libraries. Override to load specific libraries."""
        pass

    def _load_library_documentation(self, library_name: str) -> bool:
        try:
            libdoc = Libdoc(library_name)
            lib_info = libdoc.get_library_documentation()
            if not lib_info:
                return False
            keywords = [
                self._extract_keyword_from_libdoc(library_name, kw)
                for kw in lib_info.keywords
            ]
            lib_obj = RFLibraryInfo(
                name=lib_info.name,
                version=lib_info.version,
                doc=lib_info.doc,
                keywords=keywords,
            )
            self._libraries[lib_info.name] = lib_obj
            return True
        except Exception:
            return False

    def _extract_keyword_from_libdoc(self, library_name: str, kw_doc: KeywordDoc) -> RFKeywordInfo:
        args = kw_doc.args or []
        returns = kw_doc.returns
        tags = kw_doc.tags or []
        return RFKeywordInfo(
            name=kw_doc.name,
            doc=kw_doc.doc or "",
            args=args,
            returns=returns,
            tags=tags,
            library=library_name,
        )

    def _create_short_doc(self, doc: str, max_length: int = 120) -> str:
        if not doc:
            return ""
        doc = doc.strip().replace("\n", " ")
        return (doc[:max_length] + "...") if len(doc) > max_length else doc

    def find_keyword(self, keyword_name: str) -> Optional[RFKeywordInfo]:
        norm = self._normalize_name(keyword_name)
        for lib in self._libraries.values():
            for kw in lib.keywords:
                if self._normalize_name(kw.name) == norm:
                    return kw
        return None

    def get_keywords_by_library(self, library_name: str) -> List[RFKeywordInfo]:
        lib = self._libraries.get(library_name)
        return lib.keywords if lib else []

    def get_all_keywords(self) -> List[RFKeywordInfo]:
        result = []
        for lib in self._libraries.values():
            result.extend(lib.keywords)
        return result

    def get_keywords_from_libraries(self, library_names: List[str]) -> List[RFKeywordInfo]:
        result = []
        for name in library_names:
            result.extend(self.get_keywords_by_library(name))
        return result

    def search_keywords(self, pattern: str) -> List[RFKeywordInfo]:
        norm_pattern = pattern.lower()
        result = []
        for kw in self.get_all_keywords():
            if fnmatch.fnmatch(kw.name.lower(), norm_pattern):
                result.append(kw)
        return result

    def get_library_documentation(self, library_name: str) -> Optional[RFLibraryInfo]:
        return self._libraries.get(library_name)

    def get_keyword_documentation(self, keyword_name: str, library_name: str = None) -> Optional[RFKeywordInfo]:
        if library_name:
            lib = self._libraries.get(library_name)
            if lib:
                for kw in lib.keywords:
                    if self._normalize_name(kw.name) == self._normalize_name(keyword_name):
                        return kw
        else:
            return self.find_keyword(keyword_name)
        return None

    def get_keywords_documentation_all(self, keyword_name: str) -> List[RFKeywordInfo]:
        norm = self._normalize_name(keyword_name)
        result = []
        for lib in self._libraries.values():
            for kw in lib.keywords:
                if self._normalize_name(kw.name) == norm:
                    result.append(kw)
        return result

    def _normalize_name(self, name: str) -> str:
        return name.strip().lower()

    def _extract_hybrid_signature(self, keyword_name: str, library_name: str) -> Optional[List[str]]:
        # Not implemented: placeholder for hybrid keyword signature extraction
        return None

    def _is_decorated_keyword(self, args_spec) -> bool:
        # Not implemented: placeholder for decorated keyword detection
        return False

    def _extract_from_argumentspec(self, args_spec) -> List[str]:
        # Not implemented: placeholder for argument extraction
        return []

    def _extract_from_closure(self, keyword_obj, keyword_name: str, library_name: str) -> Optional[List[str]]:
        # Not implemented: placeholder for closure extraction
        return None

    def refresh_library(self, library_name: str) -> bool:
        if library_name in self._libraries:
            del self._libraries[library_name]
        return self._load_library_documentation(library_name)

    def ensure_library_loaded(self, library_name: str) -> bool:
        if library_name not in self._libraries:
            return self._load_library_documentation(library_name)
        return True

    def get_library_status(self) -> Dict[str, Any]:
        status = {}
        for lib_name in self._libraries:
            status[lib_name] = {"loaded": True}
        return status

    def is_available(self) -> bool:
        return bool(self._libraries)