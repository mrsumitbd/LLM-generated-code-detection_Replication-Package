class TeaCache:

    def __init__(self, num_inference_steps, rel_l1_thresh):
        self.num_inference_steps = num_inference_steps
        self.rel_l1_thresh = rel_l1_thresh
        self.cached_hidden_states = None
        self.cached_conditioning = None
        self.cache_valid = False

    def check(self, dit: FluxDiT, hidden_states, conditioning):
        if not self.cache_valid or self.cached_hidden_states is None:
            return False
        
        if self.cached_conditioning is None or conditioning is None:
            return False
        
        # Check if conditioning has changed significantly
        if isinstance(conditioning, dict):
            for key in conditioning:
                if key not in self.cached_conditioning:
                    return False
                cond_diff = (conditioning[key] - self.cached_conditioning[key]).abs().mean()
                if cond_diff > self.rel_l1_thresh:
                    return False
        else:
            cond_diff = (conditioning - self.cached_conditioning).abs().mean()
            if cond_diff > self.rel_l1_thresh:
                return False
        
        return True

    def store(self, hidden_states):
        if isinstance(hidden_states, dict):
            self.cached_hidden_states = {k: v.clone() if hasattr(v, 'clone') else v 
                                        for k, v in hidden_states.items()}
        elif hasattr(hidden_states, 'clone'):
            self.cached_hidden_states = hidden_states.clone()
        else:
            self.cached_hidden_states = hidden_states
        self.cache_valid = True

    def update(self, hidden_states):
        if isinstance(hidden_states, dict):
            if self.cached_hidden_states is None:
                self.cached_hidden_states = {}
            for k, v in hidden_states.items():
                if hasattr(v, 'clone'):
                    self.cached_hidden_states[k] = v.clone()
                else:
                    self.cached_hidden_states[k] = v
        elif hasattr(hidden_states, 'clone'):
            self.cached_hidden_states = hidden_states.clone()
        else:
            self.cached_hidden_states = hidden_states
        self.cache_valid = True