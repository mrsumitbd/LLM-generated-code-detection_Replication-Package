import json
from functools import partial
from cosyvoice.utils.file_utils import read_lists, read_json_lists

def Dataset(data_list_file,
            data_pipeline,
            mode='train',
            gan=False,
            shuffle=True,
            partition=True,
            tts_file='',
            prompt_utt2data=''):
    """ Construct dataset from arguments

        We have two shuffle stage in the Dataset. The first is global
        shuffle at shards tar/raw file level. The second is global shuffle
        at training samples level.

        Args:
            data_type(str): raw/shard
            tokenizer (BaseTokenizer): tokenizer to tokenize
            partition(bool): whether to do data partition in terms of rank
    """
    assert mode in ['train', 'inference']
    lists = read_lists(data_list_file)
    if mode == 'inference':
        with open(tts_file) as f:
            tts_data = json.load(f)
        utt2lists = read_json_lists(prompt_utt2data)
        # filter unnecessary file in inference mode
        lists = list({utt2lists[utt] for utt in tts_data.keys() if utt2lists[utt] in lists})
    dataset = DataList(lists,
                       shuffle=shuffle,
                       partition=partition)
    if mode == 'inference':
        # map partial arg to parquet_opener func in inference mode
        data_pipeline[0] = partial(data_pipeline[0], tts_data=tts_data)
    if gan is True:
        # map partial arg to padding func in gan mode
        data_pipeline[-1] = partial(data_pipeline[-1], gan=gan)
    for func in data_pipeline:
        dataset = Processor(dataset, func, mode=mode)
    return dataset