from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Dict, List, Optional, Any
from uuid import uuid4


@dataclass
class TextDocument:
    """
    Represents a text document with different levels of processing.
    """

    raw_text: str
    file_path: Optional[str] = None
    cleaned_text: str = ""
    sentences: List[str] = field(default_factory=list)
    words: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {
                "file_path": self.file_path,
                "encoding": "utf-8",
                "language": "russian",
                "creation_date": datetime.now().isoformat(),
                "processing_stages": [],
            }

    def get_word_count(self) -> int:
        """Returns the total number of words in the text."""
        return len(self.words)

    def get_sentence_count(self) -> int:
        """Returns the number of sentences in the text."""
        return len(self.sentences)

    def get_character_count(self) -> int:
        """Returns the number of characters in the text."""
        return len(self.raw_text)

    def add_processing_stage(self, stage: str) -> None:
        """Adds a processing step to the metadata."""
        self.metadata["processing_stages"].append(
            {"stage": stage, "timestamp": datetime.now().isoformat()}
        )


@dataclass
class StyleMetrics:
    """
    A container for all stylistic metrics of a text.
    """

    lexical_diversity: float
    formality_score: float
    readability_index: float
    pos_frequency: Dict[str, float]
    sentence_length_avg: float
    word_length_avg: float

    def to_dict(self) -> Dict[str, Any]:
        """Converts metrics to a dictionary for serialization."""
        return {
            "lexical_diversity": self.lexical_diversity,
            "formality_score": self.formality_score,
            "readability_index": self.readability_index,
            "pos_frequency": self.pos_frequency,
            "sentence_length_avg": self.sentence_length_avg,
            "word_length_avg": self.word_length_avg,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serializes metrics to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class AnalysisResult:
    """
    Aggregates text analysis results and recommendations.
    """

    text_document: TextDocument
    style_metrics: StyleMetrics
    target_style: str
    similarity_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    analysis_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    analysis_id: str = field(default_factory=lambda: str(uuid4()))

    def generate_report(self, report_format: str = "text") -> str:
        """Генерирует отчет в указанном формате."""
        if report_format == "text":
            return self._generate_text_report()
        elif report_format == "json":
            return self._generate_json_report()
        else:
            raise ValueError(f"Unsupported format: {report_format}")

    def _generate_text_report(self) -> str:
        """Generates a text report."""
        report = [
            "=" * 60,
            "АНАЛИЗ СТИЛИСТИЧЕСКОГО СООТВЕТСТВИЯ",
            "=" * 60,
            f"Целевой стиль: {self.target_style}",
            f"Соответствие: {self.similarity_score:.1%}",
            f"Дата анализа: {self.analysis_timestamp}",
            "",
            "СТИЛИСТИЧЕСКИЕ МЕТРИКИ:",
            f"  • Лексическое разнообразие: {self.style_metrics.lexical_diversity:.3f}",
            f"  • Формальность: {self.style_metrics.formality_score:.3f}",
            f"  • Удобочитаемость: {self.style_metrics.readability_index:.1f}",
            "",
            "РЕКОМЕНДАЦИИ:",
        ]

        for i, recommendation in enumerate(self.recommendations, 1):
            report.append(f"  {i}. {recommendation}")

        report.append("=" * 60)
        return "\n".join(report)

    def _generate_json_report(self) -> str:
        """Generates a JSON report."""
        report_data = {
            "analysis_id": self.analysis_id,
            "target_style": self.target_style,
            "similarity_score": self.similarity_score,
            "timestamp": self.analysis_timestamp,
            "metrics": self.style_metrics.to_dict(),
            "text_statistics": {
                "word_count": self.text_document.get_word_count(),
                "sentence_count": self.text_document.get_sentence_count(),
                "character_count": self.text_document.get_character_count(),
            },
            "recommendations": self.recommendations,
        }
        return json.dumps(report_data, indent=2, ensure_ascii=False)

    def export_to_json(self, file_path: Optional[str] = None) -> str:
        """Exports results to JSON."""
        json_report = self._generate_json_report()
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json_report)
        return json_report
