from typing import Any, List, Dict
from .task import Task
from .data_part import DataPart
from .multimodal_service import MultiModalService

class MultiModalHelper:

    @staticmethod
    def get_multimodal_service() -> MultiModalService:
        return MultiModalService()

    @staticmethod
    def has_images(task: Task) -> bool:
        return len(MultiModalHelper.extract_images(task)) > 0

    @staticmethod
    def has_documents(task: Task) -> bool:
        return len(MultiModalHelper.extract_documents(task)) > 0

    @staticmethod
    def has_multimodal_content(task: Task) -> bool:
        return MultiModalHelper.has_images(task) or MultiModalHelper.has_documents(task)

    @staticmethod
    def extract_images(task: Task) -> List[DataPart]:
        return task.get_data_parts_by_type("image")

    @staticmethod
    def extract_documents(task: Task) -> List[DataPart]:
        return task.get_data_parts_by_type("document")

    @staticmethod
    def extract_all_content(task: Task) -> Dict[str, List[Any]]:
        return {
            "images": MultiModalHelper.extract_images(task),
            "documents": MultiModalHelper.extract_documents(task)
        }

    @staticmethod
    def process_first_image(task: Task) -> Dict[str, Any] | None:
        images = MultiModalHelper.extract_images(task)
        if images:
            return MultiModalHelper.get_multimodal_service().process_image(images[0])
        return None

    @staticmethod
    def process_first_document(task: Task) -> Dict[str, Any] | None:
        documents = MultiModalHelper.extract_documents(task)
        if documents:
            return MultiModalHelper.get_multimodal_service().process_document(documents[0])
        return None

    @staticmethod
    def process_all_images(task: Task) -> List[Dict[str, Any]]:
        images = MultiModalHelper.extract_images(task)
        return [MultiModalHelper.get_multimodal_service().process_image(image) for image in images]

    @staticmethod
    def process_all_documents(task: Task) -> List[Dict[str, Any]]:
        documents = MultiModalHelper.extract_documents(task)
        return [MultiModalHelper.get_multimodal_service().process_document(document) for document in documents]

    @staticmethod
    def create_multimodal_summary(task: Task) -> str:
        summary = ""
        if MultiModalHelper.has_images(task):
            summary += "Images found. "
        if MultiModalHelper.has_documents(task):
            summary += "Documents found. "
        if not MultiModalHelper.has_multimodal_content(task):
            summary += "No multimodal content found."
        return summary.strip()