import torch
import torch.nn as nn


class CombinedTimestepGuidanceTextProjEmbeddings(nn.Module):

    def __init__(self, embedding_dim, pooled_projection_dim, data_type=torch.bfloat16):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.pooled_projection_dim = pooled_projection_dim
        self.data_type = data_type
        
        self.timestep_embedder = nn.Sequential(
            nn.Linear(1, embedding_dim),
            nn.SiLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )
        
        self.guidance_embedder = nn.Sequential(
            nn.Linear(1, embedding_dim),
            nn.SiLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )
        
        self.pooled_projection_embedder = nn.Sequential(
            nn.Linear(pooled_projection_dim, embedding_dim),
            nn.SiLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )
        
        self.combined_embedder = nn.Sequential(
            nn.Linear(embedding_dim * 3, embedding_dim * 4),
            nn.SiLU(),
            nn.Linear(embedding_dim * 4, embedding_dim)
        )

    def forward(self, timestep, guidance, pooled_projection):
        timestep = timestep.view(-1, 1).to(self.data_type)
        guidance = guidance.view(-1, 1).to(self.data_type)
        pooled_projection = pooled_projection.to(self.data_type)
        
        timestep_emb = self.timestep_embedder(timestep)
        guidance_emb = self.guidance_embedder(guidance)
        pooled_proj_emb = self.pooled_projection_embedder(pooled_projection)
        
        combined = torch.cat([timestep_emb, guidance_emb, pooled_proj_emb], dim=-1)
        output = self.combined_embedder(combined)
        
        return output