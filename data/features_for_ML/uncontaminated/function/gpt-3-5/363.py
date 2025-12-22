def has_montage(raw: MNERaw) -> bool:
    return hasattr(raw, 'info') and 'chs' in raw.info and all(hasattr(ch, 'loc') for ch in raw.info['chs'])