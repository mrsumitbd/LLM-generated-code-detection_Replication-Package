class TeaCache:
    def __init__(self, num_inference_steps, rel_l1_thresh):
        self.num_inference_steps = num_inference_steps
        self.rel_l1_thresh = rel_l1_thresh
        self.cache = {}

    def check(self, dit: FluxDiT, hidden_states, conditioning):
        key = (dit, tuple(conditioning))
        if key in self.cache:
            cached_hidden_states = self.cache[key]
            if self.compare_hidden_states(hidden_states, cached_hidden_states):
                return cached_hidden_states
        return None

    def store(self, hidden_states):
        key = (dit, tuple(conditioning))
        self.cache[key] = hidden_states

    def update(self, hidden_states):
        key = (dit, tuple(conditioning))
        if key in self.cache:
            self.cache[key] = hidden_states

    def compare_hidden_states(self, hidden_states1, hidden_states2):
        for hs1, hs2 in zip(hidden_states1, hidden_states2):
            if not self.compare_tensors(hs1, hs2):
                return False
        return True

    def compare_tensors(self, tensor1, tensor2):
        rel_l1_diff = torch.abs(tensor1 - tensor2).sum() / (torch.abs(tensor1).sum() + 1e-5)
        return rel_l1_diff < self.rel_l1_thresh