import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

class Logger:
    """簡單的日誌處理器"""
    
    def __init__(
        self,
        log_dir: str = "logs",
        level: int = logging.INFO
    ):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # 設定檔案處理器
        log_file = self.log_dir / f"translation_{datetime.now():%Y%m%d}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s'
        ))
        
        # 設定控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '[%(levelname)s] %(message)s'
        ))
        
        # 配置根日誌記錄器
        self.logger = logging.getLogger("SubtitleTranslator")
        self.logger.setLevel(level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        self.logger.info(message)
    
    def error(self, message: str, exc: Optional[Exception] = None) -> None:
        if exc:
            self.logger.error(f"{message}: {str(exc)}", exc_info=True)
        else:
            self.logger.error(message)
    
    def warning(self, message: str) -> None:
        self.logger.warning(message)
    
    def debug(self, message: str) -> None:
        self.logger.debug(message)