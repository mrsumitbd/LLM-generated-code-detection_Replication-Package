from pathlib import Path
from kreuzberg._types import (
    EasyOCRConfig,
    ExtractionConfig,
    GMFTConfig,
    HTMLToMarkdownConfig,
    OcrBackendType,
    PaddleOCRConfig,
    PSMMode,
    TesseractConfig,
)

def load_config_from_path(config_path: Path | str) -> ExtractionConfig:
    path = Path(config_path)
    config_dict = load_config_from_file(path)
    return build_extraction_config_from_dict(config_dict)