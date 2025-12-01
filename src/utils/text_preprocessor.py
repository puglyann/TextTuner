import re
from typing import List


class TextPreprocessor:
    """
    Text preprocessor that cleans, tokenizes, and normalizes text.
    """

    def __init__(self):
        self.sentence_endings = r'[.!?]+'
        self.word_pattern = r'\b[а-яё]+\b'

    def clean_text(self, text: str) -> str:
        """Clears the text from unnecessary spaces and normalizes it."""
        # Убираем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        # Нормализуем переводы строк
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def tokenize_words(self, text: str) -> List[str]:
        """Tokenizes the text into words."""
        words = re.findall(self.word_pattern, text.lower())
        return [word for word in words if len(word) > 1]

    def split_sentences(self, text: str) -> List[str]:
        """Splits the text into sentences."""
        sentences = re.split(self.sentence_endings, text)
        return [sent.strip() for sent in sentences if sent.strip()]

    def normalize_text(self, text: str) -> str:
        """Normalizes the text for analysis."""
        text = self.clean_text(text)
        return text
