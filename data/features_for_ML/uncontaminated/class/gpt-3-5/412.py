from typing import List, Optional, Dict, Any

class RobotFrameworkDocStorage:
    """Storage and retrieval of Robot Framework library documentation using native libdoc."""

    def __init__(self):
        pass

    def _initialize_libraries(self):
        pass

    def _load_library_documentation(self, library_name: str) -> bool:
        pass

    def _extract_keyword_from_libdoc(self, library_name: str, kw_doc: 'KeywordDoc') -> RFKeywordInfo:
        pass

    def _create_short_doc(self, doc: str, max_length: int = 120) -> str:
        pass

    def find_keyword(self, keyword_name: str) -> Optional[RFKeywordInfo]:
        pass

    def get_keywords_by_library(self, library_name: str) -> List[RFKeywordInfo]:
        pass

    def get_all_keywords(self) -> List[RFKeywordInfo]:
        pass

    def get_keywords_from_libraries(self, library_names: List[str]) -> List[RFKeywordInfo]:
        pass

    def search_keywords(self, pattern: str) -> List[RFKeywordInfo]:
        pass

    def get_library_documentation(self, library_name: str) -> Optional[RFLibraryInfo]:
        pass

    def get_keyword_documentation(self, keyword_name: str, library_name: str = None) -> Optional[RFKeywordInfo]:
        pass

    def get_keywords_documentation_all(self, keyword_name: str) -> List[RFKeywordInfo]:
        pass

    def _normalize_name(self, name: str) -> str:
        pass

    def _extract_hybrid_signature(self, keyword_name: str, library_name: str) -> Optional[List[str]]:
        pass

    def _is_decorated_keyword(self, args_spec) -> bool:
        pass

    def _extract_from_argumentspec(self, args_spec) -> List[str]:
        pass

    def _extract_from_closure(self, keyword_obj, keyword_name: str, library_name: str) -> Optional[List[str]]:
        pass

    def refresh_library(self, library_name: str) -> bool:
        pass

    def ensure_library_loaded(self, library_name: str) -> bool:
        pass

    def get_library_status(self) -> Dict[str, Any]:
        pass

    def is_available(self) -> bool:
        pass