from paddle.io import DistributedBatchSampler
import paddle.distributed as dist

def setup_dataloaders(config, dataloader, datamodule=None):
    if config.enable_mp or config.enable_pp:
        meshes = get_mesh()
        if meshes is None:
            raise ValueError("Mesh not initialized for MP/PP training")
        shard_dims = "dp" if config.enable_dp else None
        dataloader = dist.shard_dataloader(
            dataloader=dataloader,
            meshes=meshes,
            shard_dims=shard_dims,
        )
    elif config.enable_dp:
        train_sampler = DistributedBatchSampler(
            datamodule.train_data,
            batch_size=config.batch_size,
            shuffle=True,
            drop_last=True,
        )
        dataloader = datamodule.train_dataloader(
            num_workers=config.num_workers,
            batch_sampler=train_sampler,
        )

    return dataloader