import logging
import pprint

def dump_state(state, label: str = "Current Execution State"):
    """
    Helper method to dump the current state for debugging

    Args:
        state: Execution state to dump
        label: Optional label for the state dump
    """
    logging.info(f"[{label}]")
    logging.info(pprint.pformat(state))