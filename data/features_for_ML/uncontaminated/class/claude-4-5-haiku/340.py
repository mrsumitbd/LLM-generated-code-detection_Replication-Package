class Encoder:
    def __init__(self):
        pass
    
    def encode(self, text):
        """Encode text using base64 encoding"""
        import base64
        return base64.b64encode(text.encode()).decode()
    
    def decode(self, encoded_text):
        """Decode base64 encoded text"""
        import base64
        return base64.b64decode(encoded_text.encode()).decode()
    
    def encode_url(self, url):
        """Encode URL for safe transmission"""
        import urllib.parse
        return urllib.parse.quote(url)
    
    def decode_url(self, encoded_url):
        """Decode URL-encoded string"""
        import urllib.parse
        return urllib.parse.unquote(encoded_url)
    
    def encode_hex(self, text):
        """Encode text to hexadecimal"""
        return text.encode().hex()
    
    def decode_hex(self, hex_text):
        """Decode hexadecimal to text"""
        return bytes.fromhex(hex_text).decode()
    
    def encode_rot13(self, text):
        """Encode text using ROT13 cipher"""
        import codecs
        return codecs.encode(text, 'rot_13')
    
    def decode_rot13(self, text):
        """Decode ROT13 cipher"""
        import codecs
        return codecs.decode(text, 'rot_13')