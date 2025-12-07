from typing import Dict, Any


STYLE_CONFIGS: Dict[str, Dict[str, Any]] = {
    'научный': {
        'description': 'Научный стиль: точность, формальность, объективность',
        'target_metrics': {
            'lexical_diversity': {'target': 0.7, 'weight': 0.2, 'tolerance': 0.1},
            'formality_score': {'target': 0.8, 'weight': 0.3, 'tolerance': 0.05},
            'readability_index': {'target': 40.0, 'weight': 0.1, 'tolerance': 10.0},
            'sentence_length_avg': {'target': 15.0, 'weight': 0.2, 'tolerance': 3.0},
            'word_length_avg': {'target': 6.5, 'weight': 0.2, 'tolerance': 0.5}
        }
    },
    'художественный': {
        'description': 'Художественный стиль: выразительность, эмоциональность, образность',
        'target_metrics': {
            'lexical_diversity': {'target': 0.8, 'weight': 0.3, 'tolerance': 0.1},
            'formality_score': {'target': 0.3, 'weight': 0.2, 'tolerance': 0.1},
            'readability_index': {'target': 70.0, 'weight': 0.2, 'tolerance': 15.0},
            'sentence_length_avg': {'target': 12.0, 'weight': 0.15, 'tolerance': 4.0},
            'word_length_avg': {'target': 5.0, 'weight': 0.15, 'tolerance': 1.0}
        }
    },
    'официально-деловой': {
        'description': 'Официально-деловой стиль: стандартизированность, точность, безличность',
        'target_metrics': {
            'lexical_diversity': {'target': 0.6, 'weight': 0.15, 'tolerance': 0.1},
            'formality_score': {'target': 0.9, 'weight': 0.35, 'tolerance': 0.05},
            'readability_index': {'target': 30.0, 'weight': 0.1, 'tolerance': 10.0},
            'sentence_length_avg': {'target': 20.0, 'weight': 0.25, 'tolerance': 5.0},
            'word_length_avg': {'target': 7.0, 'weight': 0.15, 'tolerance': 0.5}
        }
    },
    'разговорный': {
        'description': 'Разговорный стиль: неформальность, простота, естественность',
        'target_metrics': {
            'lexical_diversity': {'target': 0.5, 'weight': 0.2, 'tolerance': 0.15},
            'formality_score': {'target': 0.2, 'weight': 0.3, 'tolerance': 0.1},
            'readability_index': {'target': 80.0, 'weight': 0.25, 'tolerance': 15.0},
            'sentence_length_avg': {'target': 8.0, 'weight': 0.15, 'tolerance': 3.0},
            'word_length_avg': {'target': 4.5, 'weight': 0.1, 'tolerance': 1.0}
        }
    }
}


def get_style_config(style_name: str) -> Dict[str, Any]:
    """Returns the configuration for the specified style."""
    return STYLE_CONFIGS.get(style_name.lower(), {})


def get_available_styles() -> Dict[str, str]:
    """Returns a list of available styles with descriptions."""
    return {name: config['description'] for name, config in STYLE_CONFIGS.items()}