from torch.utils.checkpoint import CheckpointPolicy, create_selective_checkpoint_contexts
import torch

def policy_fn(ctx, func, *args, **kwargs):
        mode = "recompute" if ctx.is_recompute else "forward"
        if func == torch.ops.aten.mm.default:
            op_count_key = f"{mode}_mm_count"
            # from imaginaire.utils import log
            # log.info(f"op_count_key: {op_count_key}, op_count[op_count_key]: {op_count[op_count_key]}, {args[0].shape}, {args[1].shape}")
            # there are totally 6 + 4 + 4 + 2 = 16 block
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 16
            if op_count[op_count_key] > 8:  # recompute self attn first 3 linear layers
                return CheckpointPolicy.MUST_SAVE
        if "flash_attn" in str(func):
            op_count_key = f"{mode}_flash_attn_count"
            op_count[op_count_key] = (op_count[op_count_key] + 1) % 2
            if op_count[op_count_key]:
                return CheckpointPolicy.MUST_SAVE
        return CheckpointPolicy.PREFER_RECOMPUTE