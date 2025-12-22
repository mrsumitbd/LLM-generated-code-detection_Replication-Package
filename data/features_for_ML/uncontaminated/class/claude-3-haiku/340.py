class Encoder:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.mapping = {char: str(i) for i, char in enumerate(self.alphabet)}
        self.reverse_mapping = {str(i): char for i, char in enumerate(self.alphabet)}

    def encode(self, text):
        encoded_text = ""
        for char in text.lower():
            if char in self.alphabet:
                encoded_text += self.mapping[char]
            else:
                encoded_text += char
        return encoded_text

    def decode(self, encoded_text):
        decoded_text = ""
        current_num = ""
        for char in encoded_text:
            if char in self.reverse_mapping:
                current_num += char
                if len(current_num) == 1:
                    decoded_text += self.reverse_mapping[current_num]
                    current_num = ""
            else:
                decoded_text += char
        return decoded_text