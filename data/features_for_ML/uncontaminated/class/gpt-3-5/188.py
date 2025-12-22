import torch

class CombinedTimestepGuidanceTextProjEmbeddings:

    def __init__(self, embedding_dim, pooled_projection_dim, data_type=torch.bfloat16):
        self.embedding_dim = embedding_dim
        self.pooled_projection_dim = pooled_projection_dim
        self.data_type = data_type

    def forward(self, timestep, guidance, pooled_projection):
        timestep_embedding = torch.randn(timestep.size(0), self.embedding_dim, dtype=self.data_type)
        guidance_embedding = torch.randn(guidance.size(0), self.embedding_dim, dtype=self.data_type)
        pooled_projection_embedding = torch.randn(pooled_projection.size(0), self.pooled_projection_dim, dtype=self.data_type)

        return timestep_embedding, guidance_embedding, pooled_projection_embedding