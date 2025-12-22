import os
import pickle
from typing import List, Dict, Any

def retrieval_google(
    queries: List[str],
    query_ids: List[str],
    documents: List[str],
    doc_ids: List[str],
    task: str,
    model_id: str,
    cache_dir: str,
    excluded_ids: List[str],
    long_context: bool,
    **kwargs: Any,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Simple retrieval implementation that searches local documents for query terms.
    Results are cached in `cache_dir` to avoid recomputation.

    Parameters
    ----------
    queries : List[str]
        List of query strings.
    query_ids : List[str]
        Corresponding identifiers for each query.
    documents : List[str]
        List of document texts.
    doc_ids : List[str]
        Corresponding identifiers for each document.
    task : str
        Task name (used for cache key).
    model_id : str
        Model identifier (used for cache key).
    cache_dir : str
        Directory to store cache files.
    excluded_ids : List[str]
        Document IDs to exclude from results.
    long_context : bool
        If True, return full document content; otherwise return first 200 characters.
    **kwargs : Any
        Additional keyword arguments (ignored in this implementation).

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Mapping from query_id to a list of matching documents, each represented
        as a dictionary with keys 'id' and 'content'.
    """
    # Ensure cache directory exists
    os.makedirs(cache_dir, exist_ok=True)

    # Cache file path
    cache_file = os.path.join(
        cache_dir,
        f"retrieval_google_{task}_{model_id}.pkl",
    )

    # Load from cache if available
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        except Exception:
            # If cache is corrupted, ignore and recompute
            pass

    # Build a quick lookup for documents
    doc_lookup = {did: doc for doc, did in zip(documents, doc_ids)}

    # Prepare results
    results: Dict[str, List[Dict[str, Any]]] = {}

    # Tokenize queries once for efficiency
    for q, qid in zip(queries, query_ids):
        # Lowercase query words for case-insensitive matching
        query_terms = set(q.lower().split())
        matched_docs: List[Dict[str, Any]] = []

        for did, doc in doc_lookup.items():
            if did in excluded_ids:
                continue

            # Simple containment check: any query term appears in the document
            doc_lower = doc.lower()
            if any(term in doc_lower for term in query_terms):
                content = doc if long_context else doc[:200]
                matched_docs.append({"id": did, "content": content})

        results[qid] = matched_docs

    # Cache the results
    try:
        with open(cache_file, "wb") as f:
            pickle.dump(results, f)
    except Exception:
        # If caching fails, silently ignore
        pass

    return results