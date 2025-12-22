import torch

class CombinedTimestepGuidanceTextProjEmbeddings:
    def __init__(self, embedding_dim, pooled_projection_dim, data_type=torch.bfloat16):
        super().__init__()

        self.time_proj = Timesteps(num_channels=256, flip_sin_to_cos=True, downscale_freq_shift=0)
        self.timestep_embedder = TimestepEmbedding(in_features=256, out_features=embedding_dim, data_type=data_type)
        self.guidance_embedder = TimestepEmbedding(in_features=256, out_features=embedding_dim, data_type=data_type)
        self.text_embedder = PixArtAlphaTextProjection(pooled_projection_dim, embedding_dim, act_fn="silu", data_type=data_type)

    def forward(self, timestep, guidance, pooled_projection):
        timesteps_proj = self.time_proj.forward(timestep)
        timesteps_emb = self.timestep_embedder.forward(timesteps_proj.to(dtype=pooled_projection.dtype))  # (N, D)

        guidance_proj = self.time_proj.forward(guidance)
        guidance_emb = self.guidance_embedder.forward(guidance_proj.to(dtype=pooled_projection.dtype))  # (N, D)

        time_guidance_emb = timesteps_emb + guidance_emb

        pooled_projections = self.text_embedder.forward(pooled_projection)
        conditioning = time_guidance_emb + pooled_projections

        return conditioning