class TeaCache:

    def __init__(self, num_inference_steps, rel_l1_thresh):
        self.num_inference_steps = num_inference_steps
        self.rel_l1_thresh = rel_l1_thresh
        self.cached_hidden_states = []

    def check(self, dit, hidden_states, conditioning):
        pass

    def store(self, hidden_states):
        self.cached_hidden_states.append(hidden_states)

    def update(self, hidden_states):
        pass