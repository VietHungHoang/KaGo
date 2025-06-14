from pykakasi import kakasi

class TextService:
    def __init__(self):
        kks = kakasi()
        # Configure to convert Kanji and Katakana to Hiragana
        kks.setMode("J", "H")  # Japanese to Hiragana
        self.converter = kks.getConverter()

    def normalize_japanese_text(self, text: str) -> str:
        """Convert the entire string to Hiragana and remove whitespace"""
        if not text:
            return ""
        return self.converter.do(text).strip()

    def convert_to_romaji(self, text: str) -> str:
        """Convert hiragana to romaji, comming soon!"""