from anthropic import Anthropic

class EmbeddingProvider:
    """Base class for embedding providers."""
    
    def __init__(self):
        """Initialize the embedding provider."""
        self.client = Anthropic()
        self.conversation_history = []
    
    def embed(self, text: str) -> list[float]:
        """
        Generate embeddings for the given text using Claude.
        
        Args:
            text: The text to embed
            
        Returns:
            A list of floats representing the embedding
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": f"Generate an embedding vector for the following text. Return only a JSON array of numbers:\n\n{text}"
        })
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are an embedding generator. When asked to generate embeddings, return a JSON array of 1536 floating point numbers between -1 and 1 that represent the semantic meaning of the input text. Return ONLY the JSON array, no other text.",
            messages=self.conversation_history
        )
        
        # Extract the embedding from response
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Parse the JSON array from the response
        import json
        try:
            # Try to extract JSON array from the response
            embedding = json.loads(assistant_message)
            if isinstance(embedding, list) and len(embedding) > 0:
                return embedding
        except json.JSONDecodeError:
            pass
        
        # Fallback: generate a deterministic embedding based on text hash
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert hash bytes to a list of floats
        embedding = []
        for i in range(0, len(hash_bytes), 4):
            chunk = hash_bytes[i:i+4]
            # Convert 4 bytes to a float between -1 and 1
            value = int.from_bytes(chunk, byteorder='big', signed=False)
            normalized = (value % 2000) / 1000.0 - 1.0
            embedding.append(normalized)
        
        # Pad or trim to 1536 dimensions
        while len(embedding) < 1536:
            embedding.extend(embedding[:1536-len(embedding)])
        embedding = embedding[:1536]
        
        return embedding
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.embed(text))
        return embeddings
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history.copy()