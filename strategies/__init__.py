# __init__.py

from .base import TranslationStrategy, TranslationStrategyFactory
from .quick import QuickTranslationStrategy
from .detailed import DetailedTranslationStrategy
from .keyword import KeywordExtractionStrategy

__all__ = [
    "TranslationStrategy",
    "TranslationStrategyFactory",
    "QuickTranslationStrategy",
    "DetailedTranslationStrategy",
    "KeywordExtractionStrategy"
]