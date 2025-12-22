from tqdm import tqdm,trange
from torchmetrics.functional.pairwise import pairwise_cosine_similarity
import json
import torch
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import os.path
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def retrieval_google(queries,query_ids,documents,doc_ids,task,model_id,cache_dir,excluded_ids,long_context,**kwargs):
    from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
    model = TextEmbeddingModel.from_pretrained("text-embedding-preview-0409")
    query_emb = []
    doc_emb = []
    batch_size = kwargs.get('batch_size',8)
    if not os.path.isdir(os.path.join(cache_dir, 'doc_emb', model_id, task, f"long_{long_context}_{batch_size}")):
        os.makedirs(os.path.join(cache_dir, 'doc_emb', model_id, task, f"long_{long_context}_{batch_size}"))
    for start_idx in tqdm(range(0, len(documents), batch_size), desc='embedding'):
        cur_cache_file = os.path.join(cache_dir, 'doc_emb', model_id, task, f"long_{long_context}_{batch_size}", f'{start_idx}.json')
        if os.path.isfile(cur_cache_file):
            with open(cur_cache_file) as f:
                cur_emb = json.load(f)
        else:
            cur_emb = get_embedding_google(texts=documents[start_idx:start_idx + batch_size], task='RETRIEVAL_DOCUMENT',
                                           model=model)
            with open(cur_cache_file,'w') as f:
                json.dump(cur_emb,f,indent=2)
        doc_emb += cur_emb
    for start_idx in tqdm(range(0,len(queries), batch_size),desc='embedding'):
        query_emb += get_embedding_google(texts=queries[start_idx:start_idx+ batch_size],task='RETRIEVAL_QUERY',model=model)
    scores = pairwise_cosine_similarity(torch.tensor(query_emb), torch.tensor(doc_emb))
    scores = scores.tolist()
    return get_scores(query_ids=query_ids,doc_ids=doc_ids,scores=scores,excluded_ids=excluded_ids)