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
    import os
    from torch.utils.data import IterableDataset
    
    class CustomDataset(IterableDataset):
        def __init__(self, data_list_file, data_pipeline, mode, gan, shuffle, 
                     partition, tts_file, prompt_utt2data):
            self.data_list_file = data_list_file
            self.data_pipeline = data_pipeline
            self.mode = mode
            self.gan = gan
            self.shuffle = shuffle
            self.partition = partition
            self.tts_file = tts_file
            self.prompt_utt2data = prompt_utt2data
            self.data_list = []
            self._load_data_list()
            
        def _load_data_list(self):
            """Load data list from file"""
            if os.path.exists(self.data_list_file):
                with open(self.data_list_file, 'r') as f:
                    self.data_list = [line.strip() for line in f if line.strip()]
            
            if self.shuffle:
                import random
                random.shuffle(self.data_list)
        
        def _load_tts_data(self):
            """Load TTS data if provided"""
            tts_data = {}
            if self.tts_file and os.path.exists(self.tts_file):
                with open(self.tts_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            tts_data[parts[0]] = parts[1:]
            return tts_data
        
        def _load_prompt_data(self):
            """Load prompt utterance to data mapping if provided"""
            prompt_data = {}
            if self.prompt_utt2data and os.path.exists(self.prompt_utt2data):
                with open(self.prompt_utt2data, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            prompt_data[parts[0]] = parts[1:]
            return prompt_data
        
        def __iter__(self):
            tts_data = self._load_tts_data()
            prompt_data = self._load_prompt_data()
            
            for idx, data_item in enumerate(self.data_list):
                sample = {
                    'data': data_item,
                    'index': idx,
                    'mode': self.mode,
                }
                
                if self.gan:
                    sample['gan'] = True
                
                if data_item in tts_data:
                    sample['tts'] = tts_data[data_item]
                
                if data_item in prompt_data:
                    sample['prompt'] = prompt_data[data_item]
                
                if self.data_pipeline:
                    sample = self.data_pipeline(sample)
                
                yield sample
        
        def __len__(self):
            return len(self.data_list)
    
    return CustomDataset(data_list_file, data_pipeline, mode, gan, shuffle, 
                         partition, tts_file, prompt_utt2data)