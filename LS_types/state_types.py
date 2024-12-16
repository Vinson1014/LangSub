from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

class TranslationState(Enum):
    """翻譯狀態"""
    IDLE = "idle"           # 閒置（初始狀態）
    RUNNING = "running"     # 翻譯執行中
    PAUSED = "paused"      # 已暫停
    COMPLETED = "completed" # 已完成
    ERROR = "error"        # 發生錯誤

@dataclass
class TranslationProgress:
    """翻譯進度資訊"""
    current_line: int                 # 當前處理行數
    total_lines: int                  # 總行數
    last_checkpoint: int              # 最後檢查點位置
    translated_lines: Dict[int, str]  # 已翻譯的行 {行號: 翻譯文本}
    
    def get_completion_percentage(self) -> float:
        """計算完成百分比"""
        return (self.current_line / self.total_lines * 100) if self.total_lines > 0 else 0.0
    
    def is_completed(self) -> bool:
        """檢查是否已完成所有翻譯"""
        return self.current_line >= self.total_lines

@dataclass
class StateChangeEvent:
    """狀態變更事件"""
    previous_state: TranslationState  # 前一個狀態
    current_state: TranslationState   # 當前狀態
    error_message: Optional[str] = None  # 錯誤訊息（僅在ERROR狀態時使用）