import lightning as L
from lightning.pytorch.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS
from torch.utils.data import DataLoader


def setup_dataloaders(config, dataloader, datamodule=None):
    """
    Setup dataloaders based on configuration.
    
    Args:
        config: Configuration object containing dataloader settings
        dataloader: DataLoader class or instance
        datamodule: Optional LightningDataModule instance
        
    Returns:
        Dictionary containing train, val, and test dataloaders
    """
    dataloaders = {}
    
    # If datamodule is provided, use its dataloaders
    if datamodule is not None:
        if isinstance(datamodule, L.LightningDataModule):
            # Setup the datamodule if needed
            if hasattr(datamodule, 'setup'):
                datamodule.setup()
            
            # Get dataloaders from datamodule
            if hasattr(datamodule, 'train_dataloader'):
                dataloaders['train'] = datamodule.train_dataloader()
            if hasattr(datamodule, 'val_dataloader'):
                dataloaders['val'] = datamodule.val_dataloader()
            if hasattr(datamodule, 'test_dataloader'):
                dataloaders['test'] = datamodule.test_dataloader()
    
    # If dataloader is provided and no datamodule, use it directly
    elif dataloader is not None:
        if isinstance(dataloader, DataLoader):
            dataloaders['train'] = dataloader
        elif isinstance(dataloader, dict):
            dataloaders.update(dataloader)
        elif callable(dataloader):
            # If it's a callable, try to instantiate it with config
            try:
                dataloaders['train'] = dataloader(config)
            except TypeError:
                dataloaders['train'] = dataloader()
    
    # Apply config settings if available
    if hasattr(config, 'batch_size') and 'train' in dataloaders:
        # Config batch size settings could be applied here if needed
        pass
    
    return dataloaders