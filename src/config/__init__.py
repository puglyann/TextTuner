"""
Configuration module for TextTuner.
Loads settings directly from pyproject.toml.
"""

from .style_configs import (
    STYLE_CONFIGS,
    get_style_config,
    get_available_styles,
    get_style_configs,
)

__all__ = [
    "STYLE_CONFIGS",
    "get_style_config",
    "get_available_styles",
    "get_style_configs",
]
