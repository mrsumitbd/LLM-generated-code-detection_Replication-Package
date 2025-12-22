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
            #    print_lens_blur=0.0,
               # scanner
               scan_lens_blur=0.00,
               scan_unsharp_mask=(0.7,0.7),
               output_color_space=RGBColorSpaces.sRGB,
               output_cctf_encoding=True,
            #    compute_film_raw=False,
               compute_negative=False,
               compute_full_image=False,
               )->ImageData:
    
    input_array = np.array(input_layer, dtype=np.float32) / 255.0
    
    if camera_lens_blur_um > 0:
        sigma = camera_lens_blur_um / film_format_mm * input_array.shape[1]
        input_array = gaussian_filter(input_array, sigma=sigma)
    
    if auto_exposure:
        if auto_exposure_method == AutoExposureMethods.center_weighted:
            h, w = input_array.shape[:2]
            center_region = input_array[h//4:3*h//4, w//4:3*w//4]
            target_luminance = np.mean(center_region @ np.array([0.299, 0.587, 0.114]))
        else:
            target_luminance = np.mean(input_array @ np.array([0.299, 0.587, 0.114]))
        
        exposure_ev = np.log2(0.18 / np.clip(target_luminance, 0.001, 1.0))
    else:
        exposure_ev = exposure_compensation_ev
    
    exposure_factor = 2.0 ** exposure_ev
    input_array = np.clip(input_array * exposure_factor, 0, 1)
    
    film_response = _apply_film_response(input_array, film_stock)
    
    if compute_negative:
        negative_data = ImageData(
            data=film_response,
            color_space=output_color_space,
            cctf_encoded=False
        )
    
    print_response = _apply_print_response(
        film_response,
        print_paper,
        print_illuminant,
        print_exposure,
        print_y_filter_shift,
        print_m_filter_shift
    )
    
    if print_exposure_compensation:
        print_response = np.clip(print_response * print_exposure, 0, 1)
    
    if scan_lens_blur > 0:
        print_response = gaussian_filter(print_response, sigma=scan_lens_blur)
    
    if scan_unsharp_mask[0] > 0 or scan_unsharp_mask[1] > 0:
        blurred = gaussian_filter(print_response, sigma=scan_unsharp_mask[0])
        print_response = print_response + scan_unsharp_mask[1] * (print_response - blurred)
        print_response = np.clip(print_response, 0, 1)
    
    output_array = _convert_color_space(print_response, output_color_space)
    
    if output_cctf_encoding:
        output_array = _apply_cctf(output_array, output_color_space)
    
    output_array = np.clip(output_array * 255.0, 0, 255).astype(np.uint8)
    
    result = ImageData(
        data=output_array,
        color_space=output_color_space,
        cctf_encoded=output_cctf_encoding
    )
    
    if compute_full_image:
        result.negative = negative_data if compute_negative else None
    
    return result