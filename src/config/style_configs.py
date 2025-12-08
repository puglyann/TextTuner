import tomllib
from pathlib import Path
from typing import Dict, Any


def load_config_from_pyproject() -> Dict[str, Any]:
    """Load configuration from pyproject.toml."""
    config_path = Path(__file__).parent.parent.parent / "pyproject.toml"

    if not config_path.exists():
        return {}

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        return config.get("tool", {}).get("text-tuner", {})
    except Exception:
        return {}


# Load once
_CONFIG = load_config_from_pyproject()


def get_style_configs() -> Dict[str, Dict[str, Any]]:
    """
    Get all style configurations from pyproject.toml.

    Returns:
        Dictionary with style configurations
    """
    style_configs = _CONFIG.get("styles", {})

    default_configs = {
        "научный": {"lexical_diversity": 0.7, "formality": 0.8, "readability": 40.0},
        "художественный": {
            "lexical_diversity": 0.8,
            "formality": 0.3,
            "readability": 70.0,
        },
        "официально-деловой": {
            "lexical_diversity": 0.6,
            "formality": 0.9,
            "readability": 30.0,
        },
        "разговорный": {
            "lexical_diversity": 0.5,
            "formality": 0.2,
            "readability": 80.0,
        },
    }

    for style_name, default_config in default_configs.items():
        if style_name not in style_configs:
            style_configs[style_name] = default_config

    full_configs = {}
    descriptions = {
        "научный": "Научный стиль: точность, формальность, объективность",
        "художественный": "Художественный стиль: выразительность, эмоциональность, образность",
        "официально-деловой": "Официально-деловой стиль: стандартизированность, точность, безличность",
        "разговорный": "Разговорный стиль: неформальность, простота, естественность",
    }

    for style_name, style_config in style_configs.items():
        full_configs[style_name] = {
            "description": descriptions.get(
                style_name, f"{style_name.capitalize()} стиль"
            ),
            "target_metrics": {
                "lexical_diversity": {
                    "target": style_config.get("lexical_diversity", 0.5),
                    "weight": 0.2,
                    "tolerance": 0.1,
                },
                "formality_score": {
                    "target": style_config.get("formality", 0.5),
                    "weight": 0.3,
                    "tolerance": 0.05,
                },
                "readability_index": {
                    "target": style_config.get("readability", 50.0),
                    "weight": 0.1,
                    "tolerance": 10.0,
                },
                "sentence_length_avg": {
                    "target": 15.0,
                    "weight": 0.2,
                    "tolerance": 3.0,
                },
                "word_length_avg": {"target": 6.5, "weight": 0.2, "tolerance": 0.5},
            },
        }

    return full_configs


STYLE_CONFIGS = get_style_configs()


def get_style_config(style_name: str) -> Dict[str, Any]:
    """Get configuration for specific style."""
    return STYLE_CONFIGS.get(style_name.lower(), {})


def get_available_styles() -> Dict[str, str]:
    """Get available styles with descriptions."""
    return {name: config["description"] for name, config in STYLE_CONFIGS.items()}
