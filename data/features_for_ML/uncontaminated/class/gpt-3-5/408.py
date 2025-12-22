class TextFragment:
    def __init__(self, text, style=None, link_data=None):
        self.text = text
        self.style = style
        self.link_data = link_data

    def __str__(self):
        if self.link_data:
            return f"Text: {self.text}, Style: {self.style}, Link: {self.link_data}"
        else:
            return f"Text: {self.text}, Style: {self.style}, Link: None"

# Example usage
fragment1 = TextFragment("Hello, world!")
print(fragment1)

fragment2 = TextFragment("Python is awesome!", style="bold")
print(fragment2)

fragment3 = TextFragment("Check out this link", link_data="https://www.example.com")
print(fragment3)