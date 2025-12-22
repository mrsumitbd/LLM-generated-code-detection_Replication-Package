class Encoder:
    
    def __init__(self):
        self.mapping = {}
        self.reverse_mapping = {}
    
    def encode(self, key, value):
        self.mapping[key] = value
        self.reverse_mapping[value] = key
    
    def decode_key(self, key):
        return self.mapping.get(key, None)
    
    def decode_value(self, value):
        return self.reverse_mapping.get(value, None)