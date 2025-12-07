from typing import Dict, List, Any, Tuple
import re
from dataclasses import dataclass
from collections import defaultdict

from ..models.text_models import StyleMetrics
from ..models.style_models import StyleProfile, StyleRule


@dataclass
class AdaptationRule:
    """Rule for text adaptation."""
    pattern: str
    replacement: str
    condition: Dict[str, Any]
    description: str
    style: str


class StyleAdapter:
    """
    Adapter for generating style recommendations and performing text adaptations.
    """

    def __init__(self):
        """Initialize style adapter with adaptation rules."""
        self.adaptation_rules = self._load_adaptation_rules()

    @staticmethod
    def _load_adaptation_rules() -> Dict[str, List[AdaptationRule]]:
        """Load adaptation rules for different styles."""
        return {
            'научный': [
                AdaptationRule(
                    pattern=r'\bя\b',
                    replacement='автор',
                    condition={'min_formality': 0.7},
                    description='Замена местоимения "я" на безличную форму',
                    style='научный'
                ),
                AdaptationRule(
                    pattern=r'!|\?',
                    replacement='.',
                    condition={'max_emotionality': 0.2},
                    description='Замена восклицательных и вопросительных знаков на точки',
                    style='научный'
                ),
                AdaptationRule(
                    pattern=r'\bочень\b|\bвесьма\b',
                    replacement='достаточно, значительно',
                    condition={'need_precision': True},
                    description='Замена эмоциональных наречий на более точные',
                    style='научный'
                )
            ],
            'художественный': [
                AdaptationRule(
                    pattern=r'\.',
                    replacement='...',
                    condition={'min_suspense': 0.5},
                    description='Добавление многоточий для создания напряжения',
                    style='художественный'
                ),
                AdaptationRule(
                    pattern=r'\bбыл\b|\bстал\b',
                    replacement='превратился, обернулся',
                    condition={'need_imagery': True},
                    description='Замена простых глаголов на более образные',
                    style='художественный'
                )
            ],
            'официально-деловой': [
                AdaptationRule(
                    pattern=r'\bя\b|\bмы\b',
                    replacement='нижеподписавшийся, организация',
                    condition={'need_formality': True},
                    description='Замена личных местоимений на официальные формы',
                    style='официально-деловой'
                ),
                AdaptationRule(
                    pattern=r'\bнужно\b|\bнадо\b',
                    replacement='необходимо, следует',
                    condition={'need_formality': True},
                    description='Замена разговорных форм на официальные',
                    style='официально-деловой'
                )
            ],
            'разговорный': [
                AdaptationRule(
                    pattern=r'необходимо|следует',
                    replacement='нужно, надо',
                    condition={'max_formality': 0.3},
                    description='Замена официальных форм на разговорные',
                    style='разговорный'
                ),
                AdaptationRule(
                    pattern=r'\.',
                    replacement='!',
                    condition={'min_emotionality': 0.6},
                    description='Добавление восклицательных знаков для эмоциональности',
                    style='разговорный'
                )
            ]
        }

    def generate_recommendations(self,
                                 metrics: StyleMetrics,
                                 target_profile: StyleProfile) -> List[str]:
        """
        Generate style improvement recommendations.

        Args:
            metrics (StyleMetrics): Current text metrics
            target_profile (StyleProfile): Target style profile

        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        metrics_dict = metrics.to_dict()

        for metric_name, target_config in target_profile.target_metrics.items():
            if metric_name in metrics_dict:
                current = metrics_dict[metric_name]
                target = target_config.get('target', 0)
                tolerance = target_config.get('tolerance', 0.1)

                diff = current - target

                if abs(diff) > tolerance:
                    if metric_name == 'lexical_diversity':
                        if diff < 0:
                            recommendations.append(
                                f"Увеличьте лексическое разнообразие. "
                                f"Используйте синонимы вместо повторяющихся слов."
                            )
                        else:
                            recommendations.append(
                                f"Слишком высокое лексическое разнообразие "
                                f"может снижать связность текста."
                            )

                    elif metric_name == 'formality_score':
                        if diff < 0:
                            recommendations.append(
                                f"Увеличьте формальность текста. "
                                f"Используйте термины и избегайте разговорных выражений."
                            )
                        else:
                            recommendations.append(
                                f"Снизьте формальность текста. "
                                f"Используйте более естественные, разговорные конструкции."
                            )

                    elif metric_name == 'readability_index':
                        if diff < 0:
                            recommendations.append(
                                f"Упростите текст для лучшей читаемости. "
                                f"Разбейте длинные предложения на более короткие."
                            )
                        else:
                            recommendations.append(
                                f"Текст может быть слишком упрощенным для целевого стиля. "
                                f"Добавьте более сложные конструкции."
                            )

                    elif metric_name == 'sentence_length_avg':
                        if diff < 0:
                            recommendations.append(
                                f"Увеличьте среднюю длину предложений. "
                                f"Объединяйте короткие предложения в более сложные конструкции."
                            )
                        else:
                            recommendations.append(
                                f"Слишком длинные предложения. "
                                f"Разбейте сложные предложения на более простые."
                            )

                    elif metric_name == 'word_length_avg':
                        if diff < 0:
                            recommendations.append(
                                f"Используйте более длинные, точные слова "
                                f"или специальные термины."
                            )
                        else:
                            recommendations.append(
                                f"Используйте более короткие и понятные слова."
                            )

        style_specific = self._get_style_specific_recommendations(
            target_profile.name,
            metrics_dict
        )
        recommendations.extend(style_specific)

        return recommendations[:10]  # Return top 10 recommendations

    @staticmethod
    def _get_style_specific_recommendations(style: str,
                                            metrics: Dict[str, float]) -> List[str]:
        """Get style-specific recommendations."""
        recommendations = []

        if style == 'научный':
            if metrics.get('formality_score', 0) < 0.7:
                recommendations.append(
                    "Для научного стиля используйте безличные конструкции: "
                    "'можно заключить' вместо 'я считаю'"
                )
            if metrics.get('readability_index', 0) > 50:
                recommendations.append(
                    "Усложните синтаксис: используйте причастные и деепричастные обороты"
                )

        elif style == 'художественный':
            if metrics.get('lexical_diversity', 0) < 0.7:
                recommendations.append(
                    "Используйте больше эпитетов, метафор и образных выражений"
                )
            if metrics.get('formality_score', 0) > 0.4:
                recommendations.append(
                    "Добавьте диалоги, восклицания, риторические вопросы"
                )

        elif style == 'официально-деловой':
            if metrics.get('sentence_length_avg', 0) < 15:
                recommendations.append(
                    "Используйте стандартные формулировки и клише: "
                    "'в соответствии с', 'на основании вышеизложенного'"
                )

        elif style == 'разговорный':
            if metrics.get('word_length_avg', 0) > 5:
                recommendations.append(
                    "Используйте сокращения, простые слова, междометия"
                )

        return recommendations

    def adapt_text(self,
                   text: str,
                   current_metrics: StyleMetrics,
                   target_config: Dict[str, Any]) -> str:
        """
        Adapt text to target style with automatic transformations.

        Args:
            text (str): Original text
            current_metrics (StyleMetrics): Current text metrics
            target_config (Dict): Target style configuration

        Returns:
            str: Adapted text
        """
        adapted_text = text
        style = target_config.get('description', '').split(':')[0].lower()

        if style in self.adaptation_rules:
            for rule in self.adaptation_rules[style]:
                try:
                    should_apply = self._check_rule_condition(
                        rule.condition,
                        current_metrics.to_dict(),
                        target_config
                    )

                    if should_apply:
                        adapted_text = re.sub(
                            rule.pattern,
                            rule.replacement,
                            adapted_text,
                            flags=re.IGNORECASE if rule.pattern.isalpha() else 0
                        )
                except Exception:
                    continue  # Skip rules that cause errors

        return adapted_text

    def _check_rule_condition(self,
                              condition: Dict[str, Any],
                              metrics: Dict[str, float],
                              target_config: Dict[str, Any]) -> bool:
        """Check if adaptation rule should be applied."""
        if not condition:
            return True

        for key, value in condition.items():
            if key == 'min_formality':
                if metrics.get('formality_score', 0) < value:
                    return True
            elif key == 'max_formality':
                if metrics.get('formality_score', 0) > value:
                    return True
            elif key == 'need_precision':
                return value and target_config.get('name', '') == 'научный'
            elif key == 'need_imagery':
                return value and target_config.get('name', '') == 'художественный'

        return False

    def suggest_synonyms(self, word: str, target_style: str) -> List[str]:
        """
        Suggest style-appropriate synonyms for a word.

        Args:
            word (str): Word to find synonyms for
            target_style (str): Target style

        Returns:
            List[str]: List of suggested synonyms
        """
        synonym_map = {
            'научный': {
                'большой': ['значительный', 'крупный', 'масштабный'],
                'маленький': ['незначительный', 'небольшой', 'минимальный'],
                'хороший': ['эффективный', 'оптимальный', 'удовлетворительный'],
                'плохой': ['неудовлетворительный', 'неэффективный', 'негативный'],
            },
            'художественный': {
                'большой': ['огромный', 'громадный', 'колоссальный', 'исполинский'],
                'маленький': ['крошечный', 'миниатюрный', 'малюсенький', 'небольшой'],
                'хороший': ['прекрасный', 'замечательный', 'чудесный', 'восхитительный'],
                'плохой': ['ужасный', 'отвратительный', 'скверный', 'невыносимый'],
            },
            'официально-деловой': {
                'дать': ['предоставить', 'выделить', 'назначить'],
                'взять': ['получить', 'принять', 'заимствовать'],
                'сделать': ['осуществить', 'выполнить', 'реализовать'],
                'сказать': ['сообщить', 'проинформировать', 'уведомить'],
            },
            'разговорный': {
                'человек': ['парень', 'мужик', 'тип', 'товарищ'],
                'девушка': ['девчонка', 'деваха', 'барышня'],
                'хороший': ['классный', 'клевый', 'отличный', 'нормальный'],
                'плохой': ['отстойный', 'так себе', 'не очень'],
            }
        }

        return synonym_map.get(target_style, {}).get(word.lower(), [])