import os
from typing import List

def _get_push_channels() -> List[str]:
    """
    Retrieve the list of push channels from the environment variable
    `PUSH_CHANNELS`. The variable should contain a comma‑separated list
    of channel names. If the variable is not set or empty, an empty list
    is returned.
    """
    raw = os.getenv("PUSH_CHANNELS", "")
    # Split on commas, strip whitespace, filter out empty strings
    channels = [c.strip() for c in raw.split(",") if c.strip()]
    return channels