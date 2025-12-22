from typing import Any, List, Dict

class MultiModalHelper:

    @staticmethod
    def get_multimodal_service():
        pass

    @staticmethod
    def has_images(task: Task) -> bool:
        pass

    @staticmethod
    def has_documents(task: Task) -> bool:
        pass

    @staticmethod
    def has_multimodal_content(task: Task) -> bool:
        pass

    @staticmethod
    def extract_images(task: Task) -> List[DataPart]:
        pass

    @staticmethod
    def extract_documents(task: Task) -> List[DataPart]:
        pass

    @staticmethod
    def extract_all_content(task: Task) -> Dict[str, List[Any]]:
        pass

    @staticmethod
    def process_first_image(task: Task) -> Dict[str, Any] | None:
        pass

    @staticmethod
    def process_first_document(task: Task) -> Dict[str, Any] | None:
        pass

    @staticmethod
    def process_all_images(task: Task) -> List[Dict[str, Any]]:
        pass

    @staticmethod
    def process_all_documents(task: Task) -> List[Dict[str, Any]]:
        pass

    @staticmethod
    def create_multimodal_summary(task: Task) -> str:
        pass