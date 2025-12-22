def simulation(input_layer:Image,
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
               # scanner
               scan_lens_blur=0.00,
               scan_unsharp_mask=(0.7,0.7),
               output_color_space=RGBColorSpaces.sRGB,
               output_cctf_encoding=True,
               compute_negative=False,
               compute_full_image=False,
               )->ImageData:
    
    # Implementation goes here
    pass