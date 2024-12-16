# core/state_manager.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class TranslationState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class TranslationProgress:
    current_line: int
    total_lines: int
    last_checkpoint: int
    translated_lines: Dict[int, str]  # 行號: 翻譯結果

class TranslationStateManager:
    def __init__(self):
        self.state = TranslationState.IDLE
        self.progress = None
        self._checkpoint_interval = 10  # 每翻譯10行儲存一次檢查點
        
    def start_translation(self, total_lines: int) -> None:
        self.state = TranslationState.RUNNING
        self.progress = TranslationProgress(
            current_line=0,
            total_lines=total_lines,
            last_checkpoint=0,
            translated_lines={}
        )
    
    def pause_translation(self) -> None:
        if self.state == TranslationState.RUNNING:
            self.state = TranslationState.PAUSED
            self._save_checkpoint()
    
    def resume_translation(self) -> None:
        if self.state == TranslationState.PAUSED:
            self.state = TranslationState.RUNNING
    
    def update_progress(self, line_number: int, translated_text: str) -> None:
        if self.progress is None:
            return
            
        self.progress.current_line = line_number
        self.progress.translated_lines[line_number] = translated_text
        
        if line_number - self.progress.last_checkpoint >= self._checkpoint_interval:
            self._save_checkpoint()
    
    def _save_checkpoint(self) -> None:
        if self.progress is None:
            return
        # 儲存當前進度到檢查點檔案
        self.progress.last_checkpoint = self.progress.current_line

