from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StyleProfile:
    """The profile of stylistic characteristics for each style"""
    style_name: str
    target_lexical_diversity: float
    target_formality: float
    target_readability: float
    target_pos_distribution: Dict[str, float]
    target_sentence_length: float
    characteristic_words: List[str]
    prohibited_words: List[str]

    @classmethod
    def get_style_profile(cls, style: str) -> 'StyleProfile':
        """Getting a profile for a specific style"""
        pass