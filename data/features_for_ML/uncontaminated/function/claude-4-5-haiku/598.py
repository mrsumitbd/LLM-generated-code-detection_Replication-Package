import anthropic
import json


def retrieval_google(queries, query_ids, documents, doc_ids, task, model_id, cache_dir, excluded_ids, long_context, **kwargs):
    """
    Perform retrieval tasks using Claude with prompt caching.
    
    Args:
        queries: List of query strings
        query_ids: List of query IDs
        documents: List of document strings
        doc_ids: List of document IDs
        task: Task type (e.g., "retrieval")
        model_id: Model ID to use
        cache_dir: Cache directory (not used with Anthropic API)
        excluded_ids: Set of IDs to exclude
        long_context: Whether to use long context
        **kwargs: Additional arguments
    
    Returns:
        Dictionary with results
    """
    client = anthropic.Anthropic()
    
    results = {
        "query_ids": query_ids,
        "doc_ids": doc_ids,
        "scores": []
    }
    
    # Prepare documents for context
    doc_context = "\n\n".join([
        f"Document ID: {doc_id}\nContent: {doc}" 
        for doc, doc_id in zip(documents, doc_ids)
        if doc_id not in excluded_ids
    ])
    
    # Process each query
    for query, query_id in zip(queries, query_ids):
        # Create the prompt for relevance scoring
        prompt = f"""Given the following query and documents, score the relevance of each document to the query on a scale of 0-1.

Query: {query}

Documents:
{doc_context}

For each document, provide a JSON object with the document ID and relevance score.
Return a JSON array of objects with "doc_id" and "score" fields."""
        
        # Use prompt caching for efficiency
        response = client.messages.create(
            model=model_id,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": "You are a relevance scoring assistant. Score documents based on their relevance to queries.",
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                }
            ]
        )
        
        # Parse the response
        response_text = response.content[0].text
        
        # Extract JSON from response
        try:
            # Find JSON array in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                scores_data = json.loads(json_str)
                
                # Convert to format expected by evaluation
                query_scores = {}
                for item in scores_data:
                    doc_id = item.get("doc_id")
                    score = float(item.get("score", 0))
                    if doc_id and doc_id not in excluded_ids:
                        query_scores[doc_id] = score
                
                results["scores"].append(query_scores)
            else:
                # If no JSON found, create empty scores
                results["scores"].append({})
        except (json.JSONDecodeError, ValueError, AttributeError):
            # If parsing fails, create empty scores
            results["scores"].append({})
    
    return results