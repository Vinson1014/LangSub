from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class TranslationMode(Enum):
    """翻譯模式"""
    QUICK = "quick"       # 快速翻譯
    DETAILED = "detailed" # 詳細翻譯
    KEYWORDS = "keywords" # 關鍵字提取

@dataclass
class TranslationMetadata:
    """翻譯基本設定"""
    target_language: str    # 目標語言
    region: str            # 地區設定（用於用語本地化）

@dataclass
class TranslationRequest:
    """翻譯請求"""
    text: str                     # 要翻譯的文本
    mode: TranslationMode         # 翻譯模式
    metadata: TranslationMetadata # 翻譯設定
    context: Optional[List[str]] = None  # 上下文（用於提高翻譯品質）

@dataclass
class TranslationResult:
    """翻譯結果"""
    original_text: str           # 原文
    translated_text: str         # 翻譯結果
    error_message: Optional[str] = None  # 錯誤訊息（如果有）