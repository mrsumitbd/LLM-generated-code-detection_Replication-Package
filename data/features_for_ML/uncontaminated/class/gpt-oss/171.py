from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

class MultiModalHelper:
    @staticmethod
    def get_multimodal_service() -> Any:
        """
        Return a simple multimodal service that can process images, documents and
        generate a summary. The service is defined locally to avoid external
        dependencies.
        """
        class _Service:
            def process_image(self, part: Any) -> Dict[str, Any]:
                return {"type": "image", "processed": True, "content": part.content}

            def process_document(self, part: Any) -> Dict[str, Any]:
                return {"type": "document", "processed": True, "content": part.content}

            def summarize(self, parts: List[Any]) -> str:
                return f"Summary of {len(parts)} items"

        return _Service()

    @staticmethod
    def has_images(task: Any) -> bool:
        return any(getattr(p, "type", None) == "image" for p in getattr(task, "data_parts", []))

    @staticmethod
    def has_documents(task: Any) -> bool:
        return any(getattr(p, "type", None) == "document" for p in getattr(task, "data_parts", []))

    @staticmethod
    def has_multimodal_content(task: Any) -> bool:
        return MultiModalHelper.has_images(task) or MultiModalHelper.has_documents(task)

    @staticmethod
    def extract_images(task: Any) -> List[Any]:
        return [p for p in getattr(task, "data_parts", []) if getattr(p, "type", None) == "image"]

    @staticmethod
    def extract_documents(task: Any) -> List[Any]:
        return [p for p in getattr(task, "data_parts", []) if getattr(p, "type", None) == "document"]

    @staticmethod
    def extract_all_content(task: Any) -> Dict[str, List[Any]]:
        return {
            "images": MultiModalHelper.extract_images(task),
            "documents": MultiModalHelper.extract_documents(task),
        }

    @staticmethod
    def process_first_image(task: Any) -> Optional[Dict[str, Any]]:
        images = MultiModalHelper.extract_images(task)
        if not images:
            return None
        service = MultiModalHelper.get_multimodal_service()
        return service.process_image(images[0])

    @staticmethod
    def process_first_document(task: Any) -> Optional[Dict[str, Any]]:
        docs = MultiModalHelper.extract_documents(task)
        if not docs:
            return None
        service = MultiModalHelper.get_multimodal_service()
        return service.process_document(docs[0])

    @staticmethod
    def process_all_images(task: Any) -> List[Dict[str, Any]]:
        images = MultiModalHelper.extract_images(task)
        service = MultiModalHelper.get_multimodal_service()
        return [service.process_image(p) for p in images]

    @staticmethod
    def process_all_documents(task: Any) -> List[Dict[str, Any]]:
        docs = MultiModalHelper.extract_documents(task)
        service = MultiModalHelper.get_multimodal_service()
        return [service.process_document(p) for p in docs]

    @staticmethod
    def create_multimodal_summary(task: Any) -> str:
        parts = getattr(task, "data_parts", [])
        service = MultiModalHelper.get_multimodal_service()
        return service.summarize(parts)