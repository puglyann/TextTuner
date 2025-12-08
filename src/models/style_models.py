from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from src.models import StyleMetrics


@dataclass
class StyleRule:
    """
    Defines the style adaptation rule.
    """

    rule_type: str
    condition: str
    recommendation: str
    weight: float = 1.0
    examples: List[str] = field(default_factory=list)
    category: str = "general"

    def apply_rule(self, metrics: Dict[str, Any]) -> Optional[str]:
        """Applies the rule and returns a recommendation if the condition is met."""
        try:
            if (
                self.condition == "low_formality"
                and metrics.get("formality_score", 0) < 0.3
            ):
                return self.recommendation
            elif (
                self.condition == "low_diversity"
                and metrics.get("lexical_diversity", 0) < 0.5
            ):
                return self.recommendation
        except Exception:
            return None
        return None


@dataclass
class StyleProfile:
    """
    Defines a target style with reference metrics.
    """

    name: str
    description: str
    target_metrics: Dict[str, Any]
    rules: List[StyleRule] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)

    def calculate_similarity(self, text_metrics: "StyleMetrics") -> float:
        """Calculates the degree to which the text matches the target style."""
        similarity_score = 0.0
        metrics_compared = 0

        text_dict = text_metrics.to_dict()

        for metric_name, target_config in self.target_metrics.items():
            if metric_name in text_dict:
                current_value = text_dict[metric_name]
                target_value = target_config.get("target", 0)
                weight = target_config.get("weight", 1.0)

                if target_value > 0:
                    difference = abs(current_value - target_value) / target_value
                    metric_similarity = 1 - min(difference, 1.0)
                    similarity_score += metric_similarity * weight
                    metrics_compared += weight

        return similarity_score / metrics_compared if metrics_compared > 0 else 0.0

    def validate_metrics(self, metrics: "StyleMetrics") -> Dict[str, bool]:
        """Checks which metrics match the target style."""
        validation_results = {}
        text_dict = metrics.to_dict()

        for metric_name, target_config in self.target_metrics.items():
            if metric_name in text_dict:
                current_value = text_dict[metric_name]
                target_value = target_config.get("target", 0)
                tolerance = target_config.get("tolerance", 0.1)

                validation_results[metric_name] = (
                    abs(current_value - target_value) <= tolerance
                )

        return validation_results
