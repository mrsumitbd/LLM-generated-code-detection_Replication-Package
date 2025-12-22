import os
from transformers import pipeline

def retrieval_google(queries, query_ids, documents, doc_ids, task, model_id, cache_dir, excluded_ids, long_context, **kwargs):
    # Create the retrieval pipeline
    retriever = pipeline(task, model=model_id, cache_dir=cache_dir)

    # Prepare the input data
    input_data = [{"query": q, "id": qid} for q, qid in zip(queries, query_ids)]
    corpus = [{"text": d, "id": did} for d, did in zip(documents, doc_ids)]

    # Perform the retrieval
    results = retriever(input_data, corpus=corpus, excluded_ids=excluded_ids, long_context=long_context, **kwargs)

    # Return the results
    return results