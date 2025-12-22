class Agent:

    def __init__(self, args):
        self.args = args

    def build_state(self, ob, info):
        pass

    def encode(self, observation, max_length=512):
        pass

    def decode(self, act):
        pass

    def encode_valids(self, valids, max_length=64):
        pass

    def act(self, states, valid_acts, method, state_strs=None, eps=0.1):
        pass

    def update(self, transitions, last_values, step=None, rewards_invdy=None):
        pass

    def load(self):
        pass

    def save(self):
        pass