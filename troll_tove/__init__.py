"""
Troll-Tove Fortune Teller Package

A clean, modular structure for the Troll-Tove humor-based fortune teller app.

Module Structure:
-----------------
- predictions.py: Handles loading and managing prediction content
- tone.py: Manages intro messages and text formatting with humor/dark tone
- anti_repeat.py: Implements caching to avoid repeated predictions

Design Principles:
------------------
1. Separation of concerns: Logic vs. humor vs. anti-repetition
2. Simple and readable code
3. No unnecessary abstractions or frameworks
4. Deterministic/seed-based randomness where appropriate
5. Maintains the intentionally non-serious, humorous tone
"""

from .predictions import load_predictions_from_file, PredictionSelector
from .tone import ToneFormatter
from .anti_repeat import PredictionCache, IPValidator
from .openai_client import OpenAIGenerator

__version__ = "1.0.0"

__all__ = [
    "load_predictions_from_file",
    "PredictionSelector",
    "ToneFormatter",
    "PredictionCache",
    "IPValidator",
    "OpenAIGenerator",
]
