import numpy as np
from napari.layers import Image
from napari.types import ImageData
from agx_emulsion.model.process import  photo_params, photo_process
from agx_emulsion.profiles.factory import swap_channels
from agx_emulsion.model.stocks import FilmStocks, PrintPapers, Illuminants

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
    params = photo_params(film_stock.value, print_paper.value)
    
    if special.film_channel_swap.value != (0,1,2):
        params.negative = swap_channels(params.negative, special.film_channel_swap.value)
    if special.print_channel_swap.value != (0,1,2):
        params.print_paper = swap_channels(params.print_paper, special.print_channel_swap.value)
    
    params.negative.data.tune.gamma_factor = special.film_gamma_factor.value
    params.print_paper.data.tune.gamma_factor = special.print_gamma_factor.value
    params.print_paper.data.tune.dye_density_min_factor = special.print_density_min_factor.value
    params.print_paper.glare.active = glare.active.value
    params.print_paper.glare.percent = glare.percent.value
    params.print_paper.glare.roughness = glare.roughness.value
    params.print_paper.glare.blur = glare.blur.value
    params.print_paper.glare.compensation_removal_factor = glare.compensation_removal_factor.value
    params.print_paper.glare.compensation_removal_density = glare.compensation_removal_density.value
    params.print_paper.glare.compensation_removal_transition = glare.compensation_removal_transition.value

    params.camera.lens_blur_um = camera_lens_blur_um
    params.camera.exposure_compensation_ev = exposure_compensation_ev
    params.camera.auto_exposure = auto_exposure
    params.camera.auto_exposure_method = auto_exposure_method.value
    params.camera.film_format_mm = film_format_mm
    params.camera.filter_uv = input_image.filter_uv.value
    params.camera.filter_ir = input_image.filter_ir.value
    
    params.io.preview_resize_factor = input_image.preview_resize_factor.value
    params.io.upscale_factor = input_image.upscale_factor.value
    params.io.crop = input_image.crop.value
    params.io.crop_center = input_image.crop_center.value
    params.io.crop_size = input_image.crop_size.value
    params.io.input_color_space = input_image.input_color_space.value.value
    params.io.input_cctf_decoding = input_image.apply_cctf_decoding.value
    params.io.output_color_space = output_color_space.value
    params.io.output_cctf_encoding = output_cctf_encoding
    params.io.full_image = compute_full_image
    params.io.compute_negative = compute_negative
    # params.io.compute_film_raw = compute_film_raw
    
    # assign parameters to the film stock and paper
    params.negative.halation.active = halation.active.value
    params.negative.halation.strength = np.array(halation.halation_strength.value)/100
    params.negative.halation.size_um = np.array(halation.halation_size_um.value)
    params.negative.halation.scattering_strength = np.array(halation.scattering_strength.value)/100
    params.negative.halation.scattering_size_um = np.array(halation.scattering_size_um.value)
    
    params.negative.grain.active = grain.active.value
    params.negative.grain.sublayers_active = grain.sublayers_active.value
    params.negative.grain.agx_particle_area_um2 = grain.particle_area_um2.value
    params.negative.grain.agx_particle_scale = grain.particle_scale.value
    params.negative.grain.agx_particle_scale_layers = grain.particle_scale_layers.value
    params.negative.grain.density_min = grain.density_min.value
    params.negative.grain.uniformity = grain.uniformity.value
    params.negative.grain.blur = grain.blur.value
    params.negative.grain.blur_dye_clouds_um = grain.blur_dye_clouds_um.value
    params.negative.grain.micro_structure = grain.micro_structure.value
    
    params.negative.dir_couplers.active = couplers.active.value
    params.negative.dir_couplers.amount = couplers.dir_couplers_amount.value 
    params.negative.dir_couplers.ratio_rgb = couplers.dir_couplers_ratio.value
    params.negative.dir_couplers.diffusion_size_um = couplers.dir_couplers_diffusion_um.value
    params.negative.dir_couplers.diffusion_interlayer = couplers.diffusion_interlayer.value
    params.negative.dir_couplers.high_exposure_shift = couplers.high_exposure_shift.value
        
    # # parametric curves
    # params.negative.parametric.density_curves.active = curves.use_parametric_curves.value
    # params.negative.parametric.density_curves.gamma = curves.gamma.value
    # params.negative.parametric.density_curves.log_exposure_0 = curves.log_exposure_0.value
    # params.negative.parametric.density_curves.density_max = curves.density_max.value
    # params.negative.parametric.density_curves.toe_size = curves.toe_size.value
    # params.negative.parametric.density_curves.shoulder_size = curves.shoulder_size.value

    params.enlarger.illuminant = print_illuminant.value
    params.enlarger.print_exposure = print_exposure
    params.enlarger.print_exposure_compensation = print_exposure_compensation
    params.enlarger.y_filter_shift = print_y_filter_shift
    params.enlarger.m_filter_shift = print_m_filter_shift
    # params.enlarger.print_lens_blur = print_lens_blur
    params.enlarger.preflash_exposure = preflashing.exposure.value
    params.enlarger.preflash_y_filter_shift = preflashing.y_filter_shift.value
    params.enlarger.preflash_m_filter_shift = preflashing.m_filter_shift.value
    params.enlarger.just_preflash = preflashing.just_preflash.value
    
    params.scanner.lens_blur = scan_lens_blur
    params.scanner.unsharp_mask = scan_unsharp_mask
    
    params.settings.rgb_to_raw_method = input_image.spectral_upsampling_method.value.value
    params.settings.use_camera_lut = False
    params.settings.use_enlarger_lut = True
    params.settings.use_scanner_lut = True
    params.settings.lut_resolution = 32
    params.settings.use_fast_stats = True

    image = np.double(input_layer.data[:,:,:3])
    scan = photo_process(image, params)
    # if params.io.compute_film_raw:
    #     scan = np.vstack((scan[:, :, 0], scan[:, :, 1], scan[:, :, 2]))
    scan = np.uint8(scan*255)
    return scan