from typing import Protocol, List, Optional
from dataclasses import dataclass

from services import SubtitleEvent
from LS_types import TranslationState, TranslationProgress


@dataclass
class ProgressInfo:
    """進度資訊"""
    current_batch: int       # 當前批次
    total_batches: int       # 總批次數
    current_line: int        # 當前行數
    total_lines: int         # 總行數
    current_text: str        # 當前處理文本
    translated_text: Optional[str] = None  # 翻譯後文本

@dataclass
class BatchResult:
    """批次處理結果"""
    batch_index: int                # 批次索引
    results: List[SubtitleEvent]    # 翻譯結果列表
    llm_raw_output: str             # LLM 傳回的原始輸出

class TranslationCallback(Protocol):
    """翻譯過程回調介面"""
    
    def on_progress(self, progress: ProgressInfo) -> None:
        """進度更新回調
        
        Args:
            progress: 當前進度資訊
        """
        pass
    
    def on_state_change(self, state: TranslationState) -> None:
        """狀態變更回調
        
        Args:
            state: 新的翻譯狀態
        """
        pass
    
    def on_error(self, error: Exception, current_progress: Optional[ProgressInfo] = None) -> None:
        """錯誤處理回調
        
        Args:
            error: 發生的錯誤
            current_progress: 錯誤發生時的進度資訊（可選）
        """
        pass
    
    def on_batch_complete(self, result: BatchResult) -> None:
        """批次完成回調
        
        Args:
            result: 批次處理結果
        """
        pass

class DefaultTranslationCallback(TranslationCallback):
    """預設回調實現"""
    
    def on_progress(self, progress: ProgressInfo) -> None:
        """預設進度更新處理"""
        percentage = (progress.current_line / progress.total_lines * 100)
        print(f"翻譯進度: {percentage:.1f}% ({progress.current_line}/{progress.total_lines})")
    
    def on_state_change(self, state: TranslationState) -> None:
        """預設狀態變更處理"""
        print(f"翻譯狀態變更: {state.value}")
    
    def on_error(self, error: Exception, current_progress: Optional[ProgressInfo] = None) -> None:
        """預設錯誤處理"""
        print(f"發生錯誤: {str(error)}")
        if current_progress:
            print(f"錯誤發生於第 {current_progress.current_line} 行")
    
    def on_batch_complete(self, result: BatchResult) -> None:
        """預設批次完成處理"""
        status = "有錯誤" if result.has_errors else "成功"
        print(f"批次 {result.batch_index} 處理完成: {status}")