from typing import List

class EmbeddingStoreItem:
    """嵌入库中的项"""

    def __init__(self, item_hash: str, embedding: List[float], content: str):
        self.item_hash = item_hash
        self.embedding = embedding
        self.content = content

    def to_dict(self) -> dict:
        return {
            'item_hash': self.item_hash,
            'embedding': self.embedding,
            'content': self.content
        }