import subprocess
import os
from typing import TYPE_CHECKING, Any, ClassVar, Final
from html_to_markdown._html_to_markdown import convert as rust_convert
import tempfile
from kreuzberg._utils._string import normalize_spaces
from pathlib import Path
from kreuzberg._types import ExtractionResult, HTMLToMarkdownConfig, PSMMode, TableData, TesseractConfig

def _process_image_with_tesseract(
    image_path: str,
    config_dict: dict[str, Any],
) -> dict[str, Any]:
    try:
        tesseract_format = config_dict.get("tesseract_format", "text")
        ext = config_dict.get("ext", ".txt")
        output_format = config_dict.get("output_format", "text")
        config_dict.get("enable_table_detection", False)

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
            output_base = tmp_file.name.replace(ext, "")

        try:
            language = config_dict.get("language", "eng")
            psm = config_dict.get("psm", 3)

            psm_value = psm.value if hasattr(psm, "value") else psm

            command = [
                "tesseract",
                image_path,
                output_base,
                "-l",
                language,
                "--psm",
                str(psm_value),
                "--oem",
                "1",
                "--loglevel",
                "OFF",
            ]

            if tesseract_format != "text":
                command.append(tesseract_format)

            boolean_options = [
                "classify_use_pre_adapted_templates",
                "language_model_ngram_on",
                "tessedit_dont_blkrej_good_wds",
                "tessedit_dont_rowrej_good_wds",
                "tessedit_enable_dict_correction",
                "tessedit_use_primary_params_model",
                "textord_space_size_is_variable",
                "thresholding_method",
            ]

            for option in boolean_options:
                if option in config_dict:
                    value = 1 if config_dict[option] else 0
                    command.extend(["-c", f"{option}={value}"])

            env = os.environ.copy()
            env["OMP_THREAD_LIMIT"] = "1"

            result = subprocess.run(
                command,
                check=False,
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
                encoding="utf-8",
            )

            if result.returncode != 0:
                raise Exception(f"Tesseract failed with return code {result.returncode}: {result.stderr}")

            output_file = output_base + ext
            with Path(output_file).open(encoding="utf-8") as f:
                text = f.read()

            if output_format == "markdown" and tesseract_format == "hocr":
                html_config = HTMLToMarkdownConfig(heading_style="atx")
                options, _ = html_config.to_options()
                text = rust_convert(text, options)

            text = normalize_spaces(text)

            return {
                "success": True,
                "text": text,
                "confidence": None,
                "error": None,
            }

        finally:
            for possible_ext in [ext, ".txt", ".hocr", ".tsv"]:
                temp_file = output_base + possible_ext
                temp_path = Path(temp_file)
                if temp_path.exists():
                    temp_path.unlink()

    except Exception as e:  # noqa: BLE001
        return {
            "success": False,
            "text": "",
            "confidence": None,
            "error": str(e),
        }