def check_optimizer_groups(optimizer_groups):
        for group in optimizer_groups:
            if "group_keys" not in list(group.keys()):
                raise KeyError(
                    f"key 'group_keys' was not provided in group {group}"
                )

        return optimizer_groups