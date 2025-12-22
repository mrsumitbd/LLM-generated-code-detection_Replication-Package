from typing import Any, Sequence, NamedTuple

def find_token(token_list: Sequence[int], token: str) -> Sequence[int]:
    token_ids = [index for index, value in enumerate(token_list) if value == token]

    if len(token_ids) == 0:
        raise LookupError(f'Unable to find "{token}" in token list!')

    return token_ids