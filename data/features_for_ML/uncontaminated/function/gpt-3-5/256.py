import torch

def apply_multimodal_rotary_pos_emb(q, k, cos, sin, mrope_section, unsqueeze_dim=1):
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)

    q_temporal, q_height, q_width = torch.chunk(q, mrope_section, dim=unsqueeze_dim)
    k_temporal, k_height, k_width = torch.chunk(k, mrope_section, dim=unsqueeze_dim)

    q_temporal_rot = q_temporal * cos[:, :, :mrope_section[0]] + q_height * sin[:, :, :mrope_section[0]]
    q_height_rot = q_height * cos[:, :, mrope_section[0]:mrope_section[0] + mrope_section[1]] + q_width * sin[:, :, mrope_section[0]:mrope_section[0] + mrope_section[1]]
    q_width_rot = q_width * cos[:, :, mrope_section[0] + mrope_section[1]:] + q_temporal * sin[:, :, mrope_section[0] + mrope_section[1]:]

    k_temporal_rot = k_temporal * cos[:, :, :mrope_section[0]] + k_height * sin[:, :, :mrope_section[0]]
    k_height_rot = k_height * cos[:, :, mrope_section[0]:mrope_section[0] + mrope_section[1]] + k_width * sin[:, :, mrope_section[0]:mrope_section[0] + mrope_section[1]]
    k_width_rot = k_width * cos[:, :, mrope_section[0] + mrope_section[1]:] + k_temporal * sin[:, :, mrope_section[0] + mrope_section[1]:]

    q_rot = torch.cat([q_temporal_rot, q_height_rot, q_width_rot], dim=unsqueeze_dim)
    k_rot = torch.cat([k_temporal_rot, k_height_rot, k_width_rot], dim=unsqueeze_dim)

    return q_rot, k_rot