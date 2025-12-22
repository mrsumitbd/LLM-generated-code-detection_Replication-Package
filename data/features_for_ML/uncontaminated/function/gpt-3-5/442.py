def setup_dataloaders(config, dataloader, datamodule=None):
    if datamodule is not None:
        train_loader = datamodule.train_dataloader()
        val_loader = datamodule.val_dataloader()
        test_loader = datamodule.test_dataloader()
    else:
        train_loader = dataloader(config, train=True)
        val_loader = dataloader(config, train=False, val=True)
        test_loader = dataloader(config, train=False, val=False)
    
    return train_loader, val_loader, test_loader