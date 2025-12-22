import os
from dbcan.constants.plots_constants import (
    CGC_RESULT_FILE,
    CGC_SUB_PREDICTION_FILE,
)
from dbcan.configs.plots_config import PlotsConfig

def derive_paths(cfg: PlotsConfig):
    return {
        "pul_annotation": os.path.join(cfg.input_dir, CGC_RESULT_FILE),
        "pul_substrate": os.path.join(cfg.input_dir, CGC_SUB_PREDICTION_FILE),
        "blastp": os.path.join(cfg.input_dir, "PUL_blast.out"),
    }