import re
from typing import List, Dict
from collections import Counter


class TextPreprocessor:
    """
    Text preprocessor that cleans, tokenizes, and normalizes text.
    """

    def __init__(self):
        self.sentence_endings = r"[.!?]+"
        self.word_pattern = r"\b[а-яё]+\b"
        self.stopwords = {
            "и",
            "в",
            "во",
            "не",
            "что",
            "он",
            "на",
            "я",
            "с",
            "со",
            "как",
            "а",
            "то",
            "все",
            "она",
            "так",
            "его",
            "но",
            "да",
            "ты",
            "к",
            "у",
            "же",
            "вы",
            "за",
            "бы",
            "по",
            "только",
            "ее",
            "мне",
            "было",
            "вот",
            "от",
            "меня",
            "еще",
            "нет",
            "о",
            "из",
            "ему",
            "теперь",
            "когда",
            "даже",
            "ну",
            "ли",
            "если",
            "уже",
            "или",
            "ни",
            "быть",
            "был",
            "него",
            "до",
            "вас",
            "нибудь",
            "опять",
            "уж",
            "вам",
            "ведь",
            "там",
            "потом",
            "себя",
            "ничего",
            "ей",
            "может",
            "они",
            "тут",
            "где",
            "есть",
            "надо",
            "ней",
            "для",
            "мы",
            "тебя",
            "их",
            "чем",
            "была",
            "сам",
            "чтоб",
            "без",
            "будто",
            "чего",
            "раз",
            "тоже",
            "себе",
            "под",
            "будет",
            "ж",
            "тогда",
            "кто",
            "этот",
            "того",
            "потому",
            "этого",
            "какой",
            "совсем",
            "ним",
            "здесь",
            "этом",
            "один",
            "почти",
            "мой",
            "тем",
            "чтобы",
            "нее",
            "сейчас",
            "были",
            "куда",
            "зачем",
            "всех",
            "никогда",
            "можно",
            "при",
            "наконец",
            "два",
            "об",
            "другой",
            "хоть",
            "после",
            "над",
            "больше",
            "тот",
            "через",
            "эти",
            "нас",
            "про",
            "всего",
            "них",
            "какая",
            "много",
            "разве",
            "три",
            "эту",
            "моя",
            "впрочем",
            "хорошо",
            "свою",
            "этой",
            "перед",
            "иногда",
            "лучше",
            "чуть",
            "том",
            "нельзя",
            "такой",
            "им",
            "более",
            "всегда",
            "конечно",
            "всю",
            "между",
        }

    def clean_text(self, text: str) -> str:
        """Clears the text from unnecessary spaces and normalizes it."""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Убираем лишние пробелы
        text = re.sub(r"\s+", " ", text)
        # Нормализуем переводы строк
        text = re.sub(r"\n+", "\n", text)

        # Remove extra punctuation
        text = re.sub(r"([.,!?;:-])\1+", r"\1", text)

        return text.strip()

    def tokenize_words(self, text: str, remove_stopwords: bool = False) -> List[str]:
        """Tokenizes the text into words."""
        words = re.findall(self.word_pattern, text.lower())

        if remove_stopwords:
            words = [word for word in words if word not in self.stopwords]

        # Filter short words (optional)
        words = [word for word in words if len(word) > 1]

        return words

    def split_sentences(self, text: str) -> List[str]:
        """Splits the text into sentences."""
        sentences = re.split(self.sentence_endings, text)
        return [sent.strip() for sent in sentences if sent.strip()]

    def normalize_text(self, text: str) -> str:
        """Normalizes the text for analysis."""
        text = self.clean_text(text)
        return text

    def remove_stopwords(self, words: List[str]) -> List[str]:
        """Removes stopwords from word list."""
        return [word for word in words if word not in self.stopwords]

    def get_word_frequency(self, text: str, normalize: bool = True) -> Dict[str, int]:
        """Calculates word frequency."""
        if normalize:
            text = self.normalize_text(text)

        words = self.tokenize_words(text, remove_stopwords=False)
        return dict(Counter(words))

    def extract_ngrams(self, text: str, n: int = 2) -> List[str]:
        """Extracts n-grams from text."""
        words = self.tokenize_words(text, remove_stopwords=True)

        if len(words) < n:
            return []

        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i : i + n])
            ngrams.append(ngram)

        return ngrams
