def _replace_submodules(
    root_module: nn.Module, predicate: Callable[[nn.Module], bool], func: Callable[[nn.Module], nn.Module]
) -> nn.Module:
    for name, module in root_module.named_children():
        if predicate(module):
            root_module._modules[name] = func(module)
        else:
            _replace_submodules(module, predicate, func)
    return root_module