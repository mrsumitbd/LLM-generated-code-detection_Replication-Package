def find_token(token_list: Sequence[int], token: str) -> Sequence[int]:
    return [i for i, t in enumerate(token_list) if str(t) == token]