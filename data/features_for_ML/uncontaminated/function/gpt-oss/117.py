import json
import os
import random
from typing import List, Callable, Any

import torch
from torch.utils.data import Dataset as TorchDataset


def Dataset(
    data_list_file: str,
    data_pipeline: Any,
    mode: str = "train",
    gan: bool = False,
    shuffle: bool = True,
    partition: bool = True,
    tts_file: str = "",
    prompt_utt2data: str = "",
):
    """
    Construct a PyTorch dataset from the provided arguments.

    Parameters
    ----------
    data_list_file : str
        Path to a file containing one data entry per line. Each line can be a
        JSON string or a plain text path. The function will try to parse each
        line as JSON; if that fails, the raw line is used as the data item.
    data_pipeline : Callable | List[Callable]
        A single callable or a list of callables that will be applied to each
        data item in order. Each callable should accept a data item and return
        the transformed item.
    mode : str, optional
        One of ``"train"``, ``"eval"``, ``"test"``. If a data item contains a
        ``"mode"`` key, only items matching the requested mode are kept.
    gan : bool, optional
        If True, the dataset will expose a ``gan`` attribute set to True.
    shuffle : bool, optional
        Whether to shuffle the data after loading.
    partition : bool, optional
        If True, the data will be partitioned across distributed processes
        using ``torch.distributed``. If the distributed package is not
        initialized, the dataset will not be partitioned.
    tts_file : str, optional
        Path to a JSON file mapping utterance IDs to TTS data. If provided,
        the TTS data will be merged into each data item that contains a
        matching ``"utt"`` key.
    prompt_utt2data : str, optional
        Path to a JSON file mapping utterance IDs to prompt data. If provided,
        the prompt data will be merged into each data item that contains a
        matching ``"utt"`` key.

    Returns
    -------
    TorchDataset
        A PyTorch dataset that yields processed data items.
    """

    # ------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------
    def _load_json_file(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _parse_line(line: str) -> Any:
        line = line.strip()
        if not line:
            return None
        try:
            return json.loads(line)
        except Exception:
            return line

    # ------------------------------------------------------------------
    # Load data list
    # ------------------------------------------------------------------
    if not os.path.isfile(data_list_file):
        raise FileNotFoundError(f"Data list file not found: {data_list_file}")

    raw_entries: List[Any] = []
    with open(data_list_file, "r", encoding="utf-8") as f:
        for raw_line in f:
            item = _parse_line(raw_line)
            if item is not None:
                raw_entries.append(item)

    # ------------------------------------------------------------------
    # Load optional mapping files
    # ------------------------------------------------------------------
    tts_map = {}
    if tts_file:
        if not os.path.isfile(tts_file):
            raise FileNotFoundError(f"TTS file not found: {tts_file}")
        tts_map = _load_json_file(tts_file)

    prompt_map = {}
    if prompt_utt2data:
        if not os.path.isfile(prompt_utt2data):
            raise FileNotFoundError(f"Prompt mapping file not found: {prompt_utt2data}")
        prompt_map = _load_json_file(prompt_utt2data)

    # ------------------------------------------------------------------
    # Merge mapping data into entries
    # ------------------------------------------------------------------
    processed_entries: List[Any] = []
    for entry in raw_entries:
        # If entry is a dict, we can merge
        if isinstance(entry, dict):
            utt = entry.get("utt")
            if utt:
                if utt in tts_map:
                    entry["tts"] = tts_map[utt]
                if utt in prompt_map:
                    entry["prompt"] = prompt_map[utt]
        processed_entries.append(entry)

    # ------------------------------------------------------------------
    # Filter by mode if applicable
    # ------------------------------------------------------------------
    if mode in {"train", "eval", "test"}:
        filtered_entries = []
        for entry in processed_entries:
            if isinstance(entry, dict):
                entry_mode = entry.get("mode")
                if entry_mode is None or entry_mode == mode:
                    filtered_entries.append(entry)
            else:
                # If not a dict, keep it
                filtered_entries.append(entry)
        processed_entries = filtered_entries

    # ------------------------------------------------------------------
    # Shuffle at the file level
    # ------------------------------------------------------------------
    if shuffle:
        random.shuffle(processed_entries)

    # ------------------------------------------------------------------
    # Partition across distributed processes
    # ------------------------------------------------------------------
    rank = 0
    world_size = 1
    if partition:
        try:
            import torch.distributed as dist

            if dist.is_available() and dist.is_initialized():
                rank = dist.get_rank()
                world_size = dist.get_world_size()
        except Exception:
            # Distributed not available; keep default rank/world_size
            pass

    if world_size > 1:
        processed_entries = processed_entries[rank :: world_size]

    # ------------------------------------------------------------------
    # Prepare pipeline
    # ------------------------------------------------------------------
    if not isinstance(data_pipeline, list):
        pipeline = [data_pipeline]
    else:
        pipeline = data_pipeline

    # ------------------------------------------------------------------
    # Dataset class
    # ------------------------------------------------------------------
    class CustomDataset(TorchDataset):
        def __init__(self, data: List[Any], pipeline: List[Callable]):
            self.data = data
            self.pipeline = pipeline
            self.gan = gan

        def __len__(self) -> int:
            return len(self.data)

        def __getitem__(self, idx: int) -> Any:
            item = self.data[idx]
            for func in self.pipeline:
                item = func(item)
            return item

    return CustomDataset(processed_entries, pipeline)