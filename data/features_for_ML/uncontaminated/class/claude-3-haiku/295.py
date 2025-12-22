class EmbeddingProvider:
    """Base class for embedding providers."""

    def __init__(self, model_path: str):
        self.model_path = model_path

    def get_embedding(self, text: str) -> list:
        """
        Get the embedding vector for the given text.

        Args:
            text (str): The input text.

        Returns:
            list: The embedding vector.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_batch_embedding(self, texts: list) -> list:
        """
        Get the embedding vectors for a batch of texts.

        Args:
            texts (list): A list of input texts.

        Returns:
            list: A list of embedding vectors.
        """
        return [self.get_embedding(text) for text in texts]