from collections import Counter
from typing import Dict, List

import pymorphy3

from ..models.text_models import StyleMetrics
from ..utils.text_preprocessor import TextPreprocessor
from ..utils.dictionary_loader import DictionaryLoader


class TextAnalyzer:
    """
    The main class for complex text analysis, calculation of statistical characteristics
    and determination of stylistic features.

    Attributes:
        morph_analyzer (pymorphy3.MorphAnalyzer),
        preprocessor (TextPreprocessor),
        dictionary_loader (DictionaryLoader),
        formal_words (Set[str]).
    """

    def __init__(self):
        """Initializes the text analyzer."""
        self.morph_analyzer = pymorphy3.MorphAnalyzer()
        self.preprocessor = TextPreprocessor()
        self.dictionary_loader = DictionaryLoader()
        self.formal_words = self.dictionary_loader.load_formal_dictionary()
        self.informal_words = self.dictionary_loader.load_informal_dictionary()

    def analyze_text(self, text: str) -> StyleMetrics:
        """
        Performs complex text analysis.
        Args:
            text (str): The source text to be analyzed.
        Returns:
            StyleMetrics: An object with calculated stylistic metrics.
        """
        if not text or len(text.strip()) < 10:
            raise ValueError("Текст слишком короткий для анализа")

        cleaned_text = self.preprocessor.clean_text(text)
        words = self.preprocessor.tokenize_words(cleaned_text)
        sentences = self.preprocessor.split_sentences(cleaned_text)

        lexical_diversity = self._calculate_lexical_diversity(words)
        formality_score = self._calculate_formality_score(words)
        readability_index = self._calculate_readability_index(
            cleaned_text, sentences, words
        )
        pos_frequency = self._calculate_pos_frequency(words)
        sentence_length_avg = self._calculate_sentence_length_avg(sentences)
        word_length_avg = self._calculate_word_length_avg(words)

        return StyleMetrics(
            lexical_diversity=lexical_diversity,
            formality_score=formality_score,
            readability_index=readability_index,
            pos_frequency=pos_frequency,
            sentence_length_avg=sentence_length_avg,
            word_length_avg=word_length_avg,
        )

    @staticmethod
    def _calculate_lexical_diversity(words: List[str]) -> float:
        """Calculates lexical diversity (Type-Token Ratio)."""
        if not words:
            return 0.0
        unique_words = len(set(words))
        return unique_words / len(words)

    def _calculate_formality_score(self, words: List[str]) -> float:
        """Calculates the formality score of a text."""
        if not words:
            return 0.0

        formal_count = sum(1 for word in words if word in self.formal_words)
        informal_count = sum(1 for word in words if word in self.informal_words)

        total_special = formal_count + informal_count

        if total_special == 0:
            return 0.5

        return formal_count / total_special

    @staticmethod
    def _calculate_readability_index(
        text: str, sentences: List[str], words: List[str]
    ) -> float:
        """Calculates the readability index."""
        if not sentences or not words:
            return 0.0

        avg_sentence_len = len(words) / len(sentences)
        avg_word_len = sum(len(word) for word in words) / len(words)

        readability = 206.835 - (1.3 * avg_sentence_len) - (60.1 * avg_word_len)
        return max(0.0, min(100.0, readability))

    def _calculate_pos_frequency(self, words: List[str]) -> Dict[str, float]:
        """Calculates frequencies of parts of speech."""
        pos_counter = Counter()
        total_words = len(words)

        if total_words == 0:
            return {}

        for word in words:
            try:
                parsed = self.morph_analyzer.parse(word)[0]
                pos = str(parsed.tag.POS) if parsed.tag.POS else "UNKN"
                pos_counter[pos] += 1
            except Exception:
                pos_counter["UNKN"] += 1

        return {pos: count / total_words for pos, count in pos_counter.items()}

    def _calculate_sentence_length_avg(self, sentences: List[str]) -> float:
        """Calculates the average sentence length in words."""
        if not sentences:
            return 0.0

        word_counts = []
        for sentence in sentences:
            words_in_sentence = self.preprocessor.tokenize_words(sentence)
            if words_in_sentence:
                word_counts.append(len(words_in_sentence))

        if not word_counts:
            return 0.0

        return sum(word_counts) / len(word_counts)

    @staticmethod
    def _calculate_word_length_avg(words: List[str]) -> float:
        """Calculates the average word length in characters."""
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)

    def get_text_statistics(self, text: str) -> Dict[str, any]:
        """Returns comprehensive text statistics."""
        cleaned_text = self.preprocessor.clean_text(text)
        words = self.preprocessor.tokenize_words(cleaned_text)
        sentences = self.preprocessor.split_sentences(cleaned_text)

        return {
            "total_characters": len(cleaned_text),
            "total_words": len(words),
            "total_sentences": len(sentences),
            "unique_words": len(set(words)),
            "avg_word_length": self._calculate_word_length_avg(words),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "lexical_diversity": self._calculate_lexical_diversity(words),
            "formality_score": self._calculate_formality_score(words),
        }
