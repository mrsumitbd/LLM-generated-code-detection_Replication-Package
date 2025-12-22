import torch
import torch.nn as nn
import math

class CombinedTimestepGuidanceTextProjEmbeddings(nn.Module):
    """
    Combines sinusoidal timestep embeddings, guidance embeddings, and pooled projection embeddings
    into a single embedding vector of dimension `embedding_dim`.

    Parameters
    ----------
    embedding_dim : int
        The dimensionality of the output embedding.
    pooled_projection_dim : int
        The dimensionality of the pooled projection input.
    data_type : torch.dtype, optional
        The desired data type for the embeddings (default: torch.bfloat16).
    """

    def __init__(self, embedding_dim, pooled_projection_dim, data_type=torch.bfloat16):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.pooled_projection_dim = pooled_projection_dim
        self.data_type = data_type

        # Linear projection for guidance (assumed to be a scalar or 1‑D vector)
        self.guidance_proj = nn.Linear(1, embedding_dim, bias=False)

        # Linear projection for pooled projection
        self.pooled_proj = nn.Linear(pooled_projection_dim, embedding_dim, bias=False)

    def _sinusoidal_embedding(self, timesteps):
        """
        Create a sinusoidal embedding for the given timesteps.

        Parameters
        ----------
        timesteps : torch.Tensor
            Tensor of shape (batch,) or (batch, 1) containing integer timesteps.

        Returns
        -------
        torch.Tensor
            Sinusoidal embedding of shape (batch, embedding_dim).
        """
        if timesteps.dim() == 1:
            timesteps = timesteps.unsqueeze(-1)
        device = timesteps.device
        dtype = timesteps.dtype

        # Create the frequency terms
        div_term = torch.exp(
            torch.arange(0, self.embedding_dim, 2, dtype=dtype, device=device)
            * (-math.log(10000.0) / self.embedding_dim)
        )
        # Compute sin and cos
        pos = timesteps * div_term
        sin_embed = torch.sin(pos)
        cos_embed = torch.cos(pos)
        # Interleave sin and cos
        embed = torch.empty(
            (*timesteps.shape[:-1], self.embedding_dim), dtype=dtype, device=device
        )
        embed[..., 0::2] = sin_embed
        embed[..., 1::2] = cos_embed
        return embed

    def forward(self, timestep, guidance, pooled_projection):
        """
        Forward pass to combine timestep, guidance, and pooled projection embeddings.

        Parameters
        ----------
        timestep : torch.Tensor
            Tensor of shape (batch,) or (batch, 1) containing integer timesteps.
        guidance : torch.Tensor
            Tensor of shape (batch,) or (batch, 1) containing guidance values.
        pooled_projection : torch.Tensor
            Tensor of shape (batch, pooled_projection_dim) containing pooled projection features.

        Returns
        -------
        torch.Tensor
            Combined embedding of shape (batch, embedding_dim).
        """
        # Sinusoidal timestep embedding
        timestep_emb = self._sinusoidal_embedding(timestep)

        # Guidance embedding
        if guidance.dim() == 1:
            guidance = guidance.unsqueeze(-1)
        guidance_emb = self.guidance_proj(guidance)

        # Pooled projection embedding
        pooled_emb = self.pooled_proj(pooled_projection)

        # Sum all components
        combined = timestep_emb + guidance_emb + pooled_emb

        # Cast to desired data type
        return combined.to(self.data_type)