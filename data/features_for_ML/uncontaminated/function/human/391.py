import argparse
from pathlib import Path
from omegaconf import DictConfig, ListConfig, OmegaConf

def compare(args: argparse.Namespace) -> int:
    left_path = Path(args.left).resolve()
    right_path = Path(args.right).resolve()

    # Expand via repo loader, then convert to plain dict/list so _flatten works
    left = OmegaConf.to_container(load_config(str(left_path)))  # type: ignore[assignment]
    right = OmegaConf.to_container(load_config(str(right_path)))  # type: ignore[assignment]

    lf = _flatten(left)
    rf = _flatten(right)

    left_keys = set(lf.keys())
    right_keys = set(rf.keys())

    added = sorted(right_keys - left_keys)
    removed = sorted(left_keys - right_keys)
    common = sorted(left_keys & right_keys)

    changed: list[str] = []
    for k in common:
        if lf[k] != rf[k]:
            changed.append(k)

    if not added and not removed and not changed:
        print("Configs are identical after expansion")
        return 0

    # Print concise report with explicit left/right context
    print("Comparing configs after expansion:")
    print(f"  Left : {left_path}")
    print(f"  Right: {right_path}")

    if added:
        print("\nAdded in Right (missing in Left):")
        for k in added:
            print(f"  {k} = {rf[k]}")

    if removed:
        print("\nRemoved in Right (only in Left):")
        for k in removed:
            print(f"  {k} = {lf[k]}")

    if changed:
        print("\nChanged (Left -> Right):")
        for k in changed:
            print(f"  {k}: {lf[k]} -> {rf[k]}")
    return 0