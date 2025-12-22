class MultiModalHelper:

    @staticmethod
    def get_multimodal_service():
        from anthropic import Anthropic
        return Anthropic()

    @staticmethod
    def has_images(task: Task) -> bool:
        if not hasattr(task, 'data_parts') or not task.data_parts:
            return False
        return any(part.type == 'image' for part in task.data_parts)

    @staticmethod
    def has_documents(task: Task) -> bool:
        if not hasattr(task, 'data_parts') or not task.data_parts:
            return False
        return any(part.type == 'document' for part in task.data_parts)

    @staticmethod
    def has_multimodal_content(task: Task) -> bool:
        return MultiModalHelper.has_images(task) or MultiModalHelper.has_documents(task)

    @staticmethod
    def extract_images(task: Task) -> list[DataPart]:
        if not hasattr(task, 'data_parts') or not task.data_parts:
            return []
        return [part for part in task.data_parts if part.type == 'image']

    @staticmethod
    def extract_documents(task: Task) -> list[DataPart]:
        if not hasattr(task, 'data_parts') or not task.data_parts:
            return []
        return [part for part in task.data_parts if part.type == 'document']

    @staticmethod
    def extract_all_content(task: Task) -> dict[str, list[Any]]:
        return {
            'images': MultiModalHelper.extract_images(task),
            'documents': MultiModalHelper.extract_documents(task),
            'all_parts': task.data_parts if hasattr(task, 'data_parts') else []
        }

    @staticmethod
    def process_first_image(task: Task) -> dict[str, Any] | None:
        images = MultiModalHelper.extract_images(task)
        if not images:
            return None
        image = images[0]
        return {
            'type': image.type,
            'content': image.content if hasattr(image, 'content') else None,
            'metadata': image.metadata if hasattr(image, 'metadata') else {}
        }

    @staticmethod
    def process_first_document(task: Task) -> dict[str, Any] | None:
        documents = MultiModalHelper.extract_documents(task)
        if not documents:
            return None
        document = documents[0]
        return {
            'type': document.type,
            'content': document.content if hasattr(document, 'content') else None,
            'metadata': document.metadata if hasattr(document, 'metadata') else {}
        }

    @staticmethod
    def process_all_images(task: Task) -> list[dict[str, Any]]:
        images = MultiModalHelper.extract_images(task)
        return [
            {
                'type': image.type,
                'content': image.content if hasattr(image, 'content') else None,
                'metadata': image.metadata if hasattr(image, 'metadata') else {}
            }
            for image in images
        ]

    @staticmethod
    def process_all_documents(task: Task) -> list[dict[str, Any]]:
        documents = MultiModalHelper.extract_documents(task)
        return [
            {
                'type': document.type,
                'content': document.content if hasattr(document, 'content') else None,
                'metadata': document.metadata if hasattr(document, 'metadata') else {}
            }
            for document in documents
        ]

    @staticmethod
    def create_multimodal_summary(task: Task) -> str:
        content = MultiModalHelper.extract_all_content(task)
        images_count = len(content['images'])
        documents_count = len(content['documents'])
        
        summary_parts = []
        if images_count > 0:
            summary_parts.append(f"{images_count} image(s)")
        if documents_count > 0:
            summary_parts.append(f"{documents_count} document(s)")
        
        if not summary_parts:
            return "No multimodal content"
        
        return f"Task contains: {', '.join(summary_parts)}"