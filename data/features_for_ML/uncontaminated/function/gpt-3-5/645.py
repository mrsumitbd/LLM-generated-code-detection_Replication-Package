def _replace_submodules(root_module: nn.Module, predicate: Callable[[nn.Module], bool], func: Callable[[nn.Module], nn.Module]) -> nn.Module:
    if predicate(root_module):
        return func(root_module)
    for name, module in root_module.named_children():
        setattr(root_module, name, _replace_submodules(module, predicate, func))
    return root_module