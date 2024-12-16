# strategies/base.py

from dataclasses import dataclass
from typing import Protocol, List, Optional
from LS_types import TranslationMode
from services import LLMService, SubtitleEvent
from langchain_core.messages import AIMessage

@dataclass
class ProcessResult:
    """翻譯處理結果
    
    Attributes:
        batch_result: 批次處理結果
        llm_raw_output: LLM 原始輸出
    """
    batch_result: List[SubtitleEvent]
    llm_raw_output: str

class TranslationStrategy(Protocol):
    """翻譯策略介面"""
    
    async def process(
        self,
        llm_service: LLMService,
        subtitles: List[SubtitleEvent],
        target_language: str,
        region: str,
        context: Optional[List[str]] = None,
        reference_info: Optional[str] = None,
        retry_times: int = 0,
        last_output: Optional[str] = None
    ) -> ProcessResult:
        """執行翻譯處理
        
        Args:
            llm_service: LLM 翻譯服務實例
            subtitles: 要翻譯的字幕列表
            target_language: 目標語言
            region: 地區設定
            context: 可選的上下文資訊
            reference_info: 可選的參考資訊
            
        Returns:
            處理後的字幕列表, LLM原始輸出
        """
        ...

class TranslationStrategyFactory:
    """翻譯策略工廠"""
    
    @staticmethod
    def create_strategy(mode: TranslationMode) -> TranslationStrategy:
        """根據模式創建對應的翻譯策略
        
        Args:
            mode: 翻譯模式
            
        Returns:
            對應的策略實例
        """
        from .quick import QuickTranslationStrategy
        from .detailed import DetailedTranslationStrategy
        from .keyword import KeywordExtractionStrategy
        
        strategy_map = {
            TranslationMode.QUICK: QuickTranslationStrategy(),
            TranslationMode.DETAILED: DetailedTranslationStrategy(),
            TranslationMode.KEYWORDS: KeywordExtractionStrategy()
        }
        
        return strategy_map[mode]