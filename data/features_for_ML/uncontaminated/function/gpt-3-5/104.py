def apply_gate(x, gate, tr_gate=None, tr_token=None):
    if tr_gate is None:
        return gate(x)
    else:
        return gate(x, tr_gate, tr_token)