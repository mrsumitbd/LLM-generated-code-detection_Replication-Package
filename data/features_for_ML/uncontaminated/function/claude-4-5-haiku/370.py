def dump_state(state, label: str = "Current Execution State"):
    """
    Helper method to dump the current state for debugging

    Args:
        state: Execution state to dump
        label: Optional label for the state dump
    """
    import json
    from datetime import datetime
    
    print("\n" + "="*80)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {label}")
    print("="*80)
    
    if state is None:
        print("State is None")
    elif isinstance(state, dict):
        try:
            print(json.dumps(state, indent=2, default=str))
        except (TypeError, ValueError):
            print(repr(state))
    elif isinstance(state, (list, tuple)):
        try:
            print(json.dumps(state, indent=2, default=str))
        except (TypeError, ValueError):
            print(repr(state))
    else:
        try:
            if hasattr(state, '__dict__'):
                print(json.dumps(state.__dict__, indent=2, default=str))
            else:
                print(repr(state))
        except (TypeError, ValueError):
            print(repr(state))
    
    print("="*80 + "\n")