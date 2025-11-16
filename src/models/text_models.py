from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class TextStyle(Enum):
    SCIENTIFIC = "научный"
    LITERARY = "художественный"
    OFFICIAL = "официально-деловой"
    COLLOQUIAL = "разговорный"


@dataclass
class TextStatistics:
    """Class for storing text statistics"""
    lexical_diversity: float
    formality_score: float
    readability_index: float
    pos_frequency: Dict[str, float]
    sentence_length: float
    word_length: float

    def to_dict(self) -> Dict[str, Any]:
        """Converting statistics to a dictionary"""
        pass


@dataclass
class TextAnalysis:
    """Text analysis result"""
    original_text: str
    current_style: TextStyle
    target_style: TextStyle
    statistics: TextStatistics
    recommendations: List[str]

    def get_report(self) -> str:
        """Analysis report"""
        pass