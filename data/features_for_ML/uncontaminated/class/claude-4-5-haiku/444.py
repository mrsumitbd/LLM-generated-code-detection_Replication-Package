class ChineseCangjieConverter:
    """Converts Chinese characters to Cangjie codes for tokenization."""

    def __init__(self, model_dir=None):
        self.cangjie_mapping = self._load_cangjie_mapping(model_dir)
        self.segmenter = self._init_segmenter()

    def _load_cangjie_mapping(self, model_dir=None):
        """Load Cangjie mapping from file or use default mapping."""
        cangjie_map = {}
        
        # Default Cangjie mapping for common Chinese characters
        default_mapping = {
            '中': 'lk', '国': 'mg', '人': 'o', '大': 'd', '小': 'xl',
            '山': 'u', '水': 'e', '火': 'f', '木': 'd', '金': 'c',
            '土': 'g', '日': 'a', '月': 'b', '星': 'sx', '天': 'f',
            '地': 'g', '风': 'f', '雨': 'f', '云': 'f', '雪': 'f',
            '学': 'xa', '生': 'o', '老': 'ol', '师': 'f', '父': 'f',
            '母': 'b', '子': 'nd', '女': 'v', '男': 'nm', '好': 'vd',
            '坏': 'gd', '美': 'vb', '丑': 'vb', '长': 'dl', '短': 'dl',
            '高': 'dl', '低': 'dl', '快': 'dl', '慢': 'dl', '强': 'dl',
            '弱': 'dl', '新': 'xd', '旧': 'dl', '多': 'dl', '少': 'dl',
            '有': 'vj', '无': 'vj', '是': 'vj', '非': 'vj', '对': 'vj',
            '错': 'vj', '真': 'vj', '假': 'vj', '好': 'vj', '坏': 'vj',
        }
        
        if model_dir:
            try:
                with open(f"{model_dir}/cangjie_mapping.txt", 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        if len(parts) == 2:
                            char, code = parts
                            cangjie_map[char] = code
            except (FileNotFoundError, IOError):
                cangjie_map = default_mapping
        else:
            cangjie_map = default_mapping
        
        return cangjie_map

    def _init_segmenter(self):
        """Initialize text segmenter for Chinese text."""
        try:
            import jieba
            return jieba
        except ImportError:
            return None

    def _cangjie_encode(self, glyph: str):
        """Encode a single Chinese character to Cangjie code."""
        if not glyph:
            return ""
        
        # Return mapped code if exists
        if glyph in self.cangjie_mapping:
            return self.cangjie_mapping[glyph]
        
        # For unmapped characters, generate a default code based on Unicode
        # This is a fallback mechanism
        unicode_val = ord(glyph)
        # Map Unicode value to Cangjie-like code
        cangjie_keys = 'abcdefghijklmnopqrstuvwxyz'
        code = ""
        val = unicode_val % 26
        code += cangjie_keys[val]
        
        return code

    def __call__(self, text):
        """Convert Chinese text to Cangjie codes."""
        if not text:
            return []
        
        result = []
        
        # Try to segment text if segmenter is available
        if self.segmenter:
            try:
                words = self.segmenter.cut(text)
            except Exception:
                words = list(text)
        else:
            words = list(text)
        
        # Convert each character to Cangjie code
        for word in words:
            for char in word:
                code = self._cangjie_encode(char)
                if code:
                    result.append(code)
        
        return result