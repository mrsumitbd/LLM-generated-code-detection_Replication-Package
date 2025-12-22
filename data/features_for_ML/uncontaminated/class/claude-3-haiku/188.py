import torch
import torch.nn as nn

class CombinedTimestepGuidanceTextProjEmbeddings(nn.Module):
    def __init__(self, embedding_dim, pooled_projection_dim, data_type=torch.bfloat16):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.pooled_projection_dim = pooled_projection_dim
        self.data_type = data_type

        self.timestep_embedding = nn.Embedding(1000, embedding_dim)
        self.guidance_embedding = nn.Embedding(1000, embedding_dim)
        self.projection = nn.Linear(2 * embedding_dim, pooled_projection_dim)
        self.projection.weight.data.normal_(mean=0.0, std=0.02)
        self.projection.bias.data.zero_()

    def forward(self, timestep, guidance, pooled_projection):
        timestep_emb = self.timestep_embedding(timestep).to(self.data_type)
        guidance_emb = self.guidance_embedding(guidance).to(self.data_type)
        combined_emb = torch.cat([timestep_emb, guidance_emb], dim=-1)
        output = self.projection(combined_emb)
        return output