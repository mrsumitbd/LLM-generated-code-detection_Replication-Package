import torch.nn as nn
from typing import Callable

def _replace_submodules(
    root_module: nn.Module,
    predicate: Callable[[nn.Module], bool],
    func: Callable[[nn.Module], nn.Module]
) -> nn.Module:
    """
    Recursively replace submodules of `root_module` that satisfy `predicate`
    with the module returned by `func`.

    Args:
        root_module: The module for which the submodules need to be replaced.
        predicate: Takes a module as an argument and must return True if that
            module is to be replaced.
        func: Takes a module as an argument and returns a new module to replace
            it with.

    Returns:
        The root module with its submodules replaced.
    """
    # If the root itself matches, replace it and return the new root
    if predicate(root_module):
        return func(root_module)

    # Helper to recursively replace children
    def _replace(module: nn.Module):
        for name, child in list(module.named_children()):
            if predicate(child):
                # Replace the child module
                new_child = func(child)
                setattr(module, name, new_child)
            else:
                # Recurse into the child
                _replace(child)

    _replace(root_module)
    return root_module