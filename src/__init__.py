__version__ = "1.0.0"
__author__ = "Anna Azimkova"
__email__ = "adazimkova@edu.hse.ru"

from .core.text_analyzer import TextAnalyzer
from .core.style_adapter import StyleAdapter
from .core.statistics_calculator import StatisticsCalculator
from .models.text_models import TextDocument, StyleMetrics, AnalysisResult
from .models.style_models import StyleProfile, StyleRule

__all__ = [
    'TextAnalyzer',
    'StyleAdapter',
    'StatisticsCalculator',
    'TextDocument',
    'StyleMetrics',
    'AnalysisResult',
    'StyleProfile',
    'StyleRule',
]
