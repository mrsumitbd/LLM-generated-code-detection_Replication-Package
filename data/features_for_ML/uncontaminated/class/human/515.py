
class PromptFormatter:
    def __init__(self, t2i, opt):
        self.t2i = t2i
        self.opt = opt

    # note: the t2i object should provide all these values.
    # there should be no need to or against opt values
    def normalize_prompt(self):
        """Normalize the prompt and switches"""
        t2i = self.t2i
        opt = self.opt

        switches = []
        switches.append(f'"{opt.prompt}"')
        switches.append(f"-s{opt.steps        or t2i.steps}")
        switches.append(f"-W{opt.width        or t2i.width}")
        switches.append(f"-H{opt.height       or t2i.height}")
        switches.append(f"-C{opt.cfg_scale    or t2i.cfg_scale}")
        switches.append(f"-A{opt.sampler_name or t2i.sampler_name}")
        # to do: put model name into the t2i object
        #        switches.append(f'--model{t2i.model_name}')
        if opt.seamless or t2i.seamless:
            switches.append("--seamless")
        if opt.init_img:
            switches.append(f"-I{opt.init_img}")
        if opt.fit:
            switches.append("--fit")
        if opt.strength and opt.init_img is not None:
            switches.append(f"-f{opt.strength or t2i.strength}")
        if opt.gfpgan_strength:
            switches.append(f"-G{opt.gfpgan_strength}")
        if opt.upscale:
            switches.append(f'-U {" ".join([str(u) for u in opt.upscale])}')
        if opt.variation_amount > 0:
            switches.append(f"-v{opt.variation_amount}")
        if opt.with_variations:
            formatted_variations = ",".join(f"{seed}:{weight}" for seed, weight in opt.with_variations)
            switches.append(f"-V{formatted_variations}")
        return " ".join(switches)