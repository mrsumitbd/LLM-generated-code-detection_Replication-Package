import torch
import itertools

def create_optimizer(
    model: TrainableDecoder,
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
):
    """Create optimizers for generator and discriminator."""
    # in the generator, keep vq quantizer frozen.

    gen_params = itertools.chain(
        model.generator.decoder.backbone.parameters(),
        model.generator.upsampler.parameters() if model.generator.upsampler else [],
        model.generator.decoder.head.parameters(),
        model.generator.fc_post_a.parameters(),
    )
    gen_optimizer = torch.optim.AdamW(
        gen_params, lr=learning_rate, betas=betas, weight_decay=weight_decay
    )

    # discriminators.
    disc_params = itertools.chain(model.mpd.parameters(), model.msd.parameters())
    disc_optimizer = torch.optim.AdamW(
        disc_params, lr=learning_rate, betas=betas, weight_decay=weight_decay
    )
    return gen_optimizer, disc_optimizer