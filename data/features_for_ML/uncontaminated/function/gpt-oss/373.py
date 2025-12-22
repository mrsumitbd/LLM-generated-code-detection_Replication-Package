from typing import Any, Sequence, Dict, List
import numpy as np

try:
    import torch
except ImportError:
    torch = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    from datasets import Dataset
except ImportError:
    Dataset = None

# The following imports are expected to be available in the environment
# where this function is used. They are imported lazily to avoid
# unnecessary dependencies when the function is not called.
try:
    from .constants import DEFAULT_FINETUNE_EXAMPLE_TEMPLATE, ReturnType
except Exception:
    # Fallback definitions for standalone usage
    DEFAULT_FINETUNE_EXAMPLE_TEMPLATE = (
        "### Question:\n{query}\n\n### Answer:\n{answer}\n\n### End"
    )

    class ReturnType:
        PYTORCH = "pytorch"
        TENSORFLOW = "tensorflow"
        HUGGINGFACE = "huggingface"


def build_finetune_dataset(
    rag_system: Any,
    examples: Sequence[Dict[str, str]],
    eos_token_id: int,
    finetune_example_template: str = DEFAULT_FINETUNE_EXAMPLE_TEMPLATE,
    query_key: str = "query",
    answer_key: str = "answer",
    return_dataset: ReturnType = ReturnType.PYTORCH,
) -> Any:
    """
    Generates the finetuning dataset using the supplied rag_system and examples.

    Parameters
    ----------
    rag_system : Any
        An object that exposes a `tokenizer` attribute compatible with the
        HuggingFace tokenizer API.
    examples : Sequence[dict]
        A sequence of dictionaries containing at least the keys specified by
        `query_key` and `answer_key`.
    eos_token_id : int
        The token id that should be appended to each example.
    finetune_example_template : str, optional
        A format string that receives `query` and `answer` as keyword arguments.
    query_key : str, optional
        Key used to extract the query from each example.
    answer_key : str, optional
        Key used to extract the answer from each example.
    return_dataset : ReturnType, optional
        The type of dataset to return. One of `ReturnType.PYTORCH`,
        `ReturnType.TENSORFLOW`, or `ReturnType.HUGGINGFACE`.

    Returns
    -------
    Any
        A dataset object in the requested format.
    """
    if not hasattr(rag_system, "tokenizer"):
        raise ValueError("rag_system must expose a `tokenizer` attribute")

    tokenizer = rag_system.tokenizer

    # Prepare raw texts
    raw_texts = []
    for ex in examples:
        query = ex.get(query_key, "")
        answer = ex.get(answer_key, "")
        raw_texts.append(finetune_example_template.format(query=query, answer=answer))

    # Tokenize all examples
    tokenized = tokenizer(
        raw_texts,
        add_special_tokens=False,
        return_attention_mask=True,
        return_tensors=None,
        truncation=False,
        padding=False,
    )

    input_ids_list: List[List[int]] = tokenized["input_ids"]
    attention_mask_list: List[List[int]] = tokenized["attention_mask"]

    # Append EOS token to each example
    for idx, ids in enumerate(input_ids_list):
        input_ids_list[idx] = ids + [eos_token_id]
        attention_mask_list[idx] = attention_mask_list[idx] + [1]

    # Determine max length for padding
    max_len = max(len(ids) for ids in input_ids_list)

    pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else 0

    # Pad input_ids, attention_mask, and labels
    padded_input_ids = []
    padded_attention_mask = []
    padded_labels = []

    for ids, mask in zip(input_ids_list, attention_mask_list):
        pad_len = max_len - len(ids)
        padded_input_ids.append(ids + [pad_token_id] * pad_len)
        padded_attention_mask.append(mask + [0] * pad_len)
        # Labels are the same as input_ids, but pad with pad_token_id
        padded_labels.append(ids + [pad_token_id] * pad_len)

    # Convert to numpy arrays
    input_ids_np = np.array(padded_input_ids, dtype=np.int32)
    attention_mask_np = np.array(padded_attention_mask, dtype=np.int32)
    labels_np = np.array(padded_labels, dtype=np.int32)

    if return_dataset == ReturnType.PYTORCH:
        if torch is None:
            raise ImportError("PyTorch is not installed")
        return {
            "input_ids": torch.tensor(input_ids_np),
            "attention_mask": torch.tensor(attention_mask_np),
            "labels": torch.tensor(labels_np),
        }

    if return_dataset == ReturnType.TENSORFLOW:
        if tf is None:
            raise ImportError("TensorFlow is not installed")
        return {
            "input_ids": tf.convert_to_tensor(input_ids_np, dtype=tf.int32),
            "attention_mask": tf.convert_to_tensor(attention_mask_np, dtype=tf.int32),
            "labels": tf.convert_to_tensor(labels_np, dtype=tf.int32),
        }

    if return_dataset == ReturnType.HUGGINGFACE:
        if Dataset is None:
            raise ImportError("datasets library is not installed")
        return Dataset.from_dict(
            {
                "input_ids": input_ids_np.tolist(),
                "attention_mask": attention_mask_np.tolist(),
                "labels": labels_np.tolist(),
            }
        )

    raise ValueError(f"Unsupported return_dataset type: {return_dataset}")