def _hacked_flash_attention_forward(*args,**kwargs):
        global HACKED_POSITION_IDS
        if HACKED_POSITION_IDS is not None:
            kwargs['position_ids'] = HACKED_POSITION_IDS
        return raw_flash_attention_forward(*args,**kwargs)