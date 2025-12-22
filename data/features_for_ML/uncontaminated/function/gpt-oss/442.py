def setup_dataloaders(config, dataloader, datamodule=None):
    """
    Create train/validation/test dataloaders from either a datamodule or a
    dataloader factory.

    Parameters
    ----------
    config : dict
        Configuration dictionary that may contain dataset paths, batch size,
        etc.
    dataloader : callable or class
        A factory that, when called with ``config``, returns an object that
        provides ``train_dataloader()``, ``val_dataloader()`` and
        ``test_dataloader()`` methods, or a mapping with keys ``'train'``,
        ``'val'`` and ``'test'``.
    datamodule : object, optional
        If provided, it is expected to have ``train_dataloader()``,
        ``val_dataloader()`` and ``test_dataloader()`` methods.

    Returns
    -------
    tuple
        (train_loader, val_loader, test_loader)
    """
    # If a datamodule is supplied, use it directly
    if datamodule is not None:
        train_loader = datamodule.train_dataloader()
        val_loader = datamodule.val_dataloader()
        test_loader = datamodule.test_dataloader()
        return train_loader, val_loader, test_loader

    # Otherwise, use the dataloader factory
    loader_obj = dataloader(config)

    # If the returned object has the expected methods, use them
    if hasattr(loader_obj, "train_dataloader") and hasattr(loader_obj, "val_dataloader") and hasattr(loader_obj, "test_dataloader"):
        train_loader = loader_obj.train_dataloader()
        val_loader = loader_obj.val_dataloader()
        test_loader = loader_obj.test_dataloader()
        return train_loader, val_loader, test_loader

    # Fallback: assume the object is a mapping with the loaders
    train_loader = loader_obj.get("train") if isinstance(loader_obj, dict) else None
    val_loader = loader_obj.get("val") if isinstance(loader_obj, dict) else None
    test_loader = loader_obj.get("test") if isinstance(loader_obj, dict) else None
    return train_loader, val_loader, test_loader