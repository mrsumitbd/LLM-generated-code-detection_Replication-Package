class MockCompletion:
    def __init__(self):
        self.choices = []
        self.usage = 0

    def add_choice(self, text, score):
        self.choices.append({"text": text, "score": score})

    def get_top_choice(self):
        if not self.choices:
            return None
        self.choices.sort(key=lambda x: x["score"], reverse=True)
        self.usage += 1
        return self.choices[0]

    def get_usage(self):
        return self.usage