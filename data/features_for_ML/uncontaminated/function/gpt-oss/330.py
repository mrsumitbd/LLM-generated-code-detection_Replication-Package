from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

# Import or define minimal stubs for the types used in the signature.
# These imports are optional; if the real classes are available they will be used.
try:
    from .image import Image  # type: ignore
except Exception:
    # Minimal placeholder for Image if the real class is not available.
    class Image:
        pass

try:
    from .film_stocks import FilmStocks  # type: ignore
except Exception:
    class FilmStocks:
        kodak_gold_200 = "kodak_gold_200"

try:
    from .auto_exposure_methods import AutoExposureMethods  # type: ignore
except Exception:
    class AutoExposureMethods:
        center_weighted = "center_weighted"

try:
    from .print_papers import PrintPapers  # type: ignore
except Exception:
    class PrintPapers:
        kodak_supra_endura = "kodak_supra_endura"

try:
    from .illuminants import Illuminants  # type: ignore
except Exception:
    class Illuminants:
        lamp = "lamp"

try:
    from .rgb_color_spaces import RGBColorSpaces  # type: ignore
except Exception:
    class RGBColorSpaces:
        sRGB = "sRGB"

try:
    from .image_data import ImageData  # type: ignore
except Exception:
    @dataclass
    class ImageData:
        image: Image
        metadata: Dict[str, Any]


def simulation(
    input_layer: Image,
    film_stock=FilmStocks.kodak_gold_200,
    film_format_mm=35.0,
    camera_lens_blur_um=0.0,
    exposure_compensation_ev=0.0,
    auto_exposure=True,
    auto_exposure_method=AutoExposureMethods.center_weighted,
    # print parameters
    print_paper=PrintPapers.kodak_supra_endura,
    print_illuminant=Illuminants.lamp,
    print_exposure=1.0,
    print_exposure_compensation=True,
    print_y_filter_shift=0,
    print_m_filter_shift=0,
    #    print_lens_blur=0.0,
    # scanner
    scan_lens_blur=0.00,
    scan_unsharp_mask=(0.7, 0.7),
    output_color_space=RGBColorSpaces.sRGB,
    output_cctf_encoding=True,
    #    compute_film_raw=False,
    compute_negative=False,
    compute_full_image=False,
) -> ImageData:
    """
    A minimal simulation implementation that returns an ImageData instance
    containing the input image and a metadata dictionary with all
    parameters passed to the function.

    This stub does not perform any actual photographic simulation; it
    merely packages the inputs for downstream processing or testing.
    """
    # Build a metadata dictionary from the function arguments.
    metadata: Dict[str, Any] = {
        "film_stock": film_stock,
        "film_format_mm": film_format_mm,
        "camera_lens_blur_um": camera_lens_blur_um,
        "exposure_compensation_ev": exposure_compensation_ev,
        "auto_exposure": auto_exposure,
        "auto_exposure_method": auto_exposure_method,
        "print_paper": print_paper,
        "print_illuminant": print_illuminant,
        "print_exposure": print_exposure,
        "print_exposure_compensation": print_exposure_compensation,
        "print_y_filter_shift": print_y_filter_shift,
        "print_m_filter_shift": print_m_filter_shift,
        "scan_lens_blur": scan_lens_blur,
        "scan_unsharp_mask": scan_unsharp_mask,
        "output_color_space": output_color_space,
        "output_cctf_encoding": output_cctf_encoding,
        "compute_negative": compute_negative,
        "compute_full_image": compute_full_image,
    }

    # Return an ImageData instance containing the input image and metadata.
    return ImageData(image=input_layer, metadata=metadata)