"""
TextTuner is a tool for adapting text to a target style.

The main module of the application provides an interface for analyzing and adapting text.
"""

import sys
import os
from typing import Optional

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.text_analyzer import TextAnalyzer
from src.core.style_adapter import StyleAdapter
# from src.models.text_models import TextDocument, AnalysisResult
from src.utils.file_handler import FileHandler


class TextTuner:
    """
    The main class of the TextTuner application.

    Coordinates the operation of all system components: file reading, text analysis,
    style adaptation, and report generation.

    Attributes:
    text_analyzer (TextAnalyzer): Text analyzer.
    style_adapter (StyleAdapter): Style adapter.
    file_handler (FileHandler): File handler.
    """



