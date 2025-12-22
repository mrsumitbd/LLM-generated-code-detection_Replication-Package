from typing import List, Tuple, Union

def promise_batch_action_add_key_with_full_access(
    promise_index: int, public_key: Union[bytes, str], nonce: int
) -> None:
    """
    Add an "add full access key" action to the given promise batch.

    Args:
        promise_index: The index of the promise batch
        public_key: The public key to add (borsh-serialized)
        nonce: The nonce for the key

    Note:
        This is a mock function in the local environment and has no effect.
    """
    pass