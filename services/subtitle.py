from pathlib import Path
from typing import List, Dict
import pysubs2
import chardet
from dataclasses import dataclass

@dataclass
class SubtitleEvent:
    """字幕事件資料結構"""
    index: int
    start: int  # 毫秒
    end: int    # 毫秒
    text: str
    translation_text: str = ""  # 改為空字串作為預設值，因為必定會被更新

class SubtitleHandlerError(Exception):
    """字幕處理相關錯誤"""
    pass

class EncodingError(SubtitleHandlerError):
    """編碼相關錯誤"""
    pass

class FileAccessError(SubtitleHandlerError):
    """檔案存取相關錯誤"""
    pass

class SubtitleHandler:
    def __init__(self):
        self.supported_formats = ['.srt', '.ass', '.ssa']
        self.common_encodings = ['utf-8', 'big5', 'gb18030', 'shift-jis', 'euc-kr']
        
    def detect_encoding(self, file_path: str) -> str:
        """檢測檔案編碼"""
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                return result['encoding']
        except Exception as e:
            raise FileAccessError(f"無法讀取檔案進行編碼檢測: {str(e)}")
    
    def read_subtitle(self, file_path: str) -> List[SubtitleEvent]:
        """讀取字幕檔案並轉換為標準格式"""
        if not self.validate_file(file_path):
            raise ValueError(f"不支援的檔案格式: {file_path}")
            
        try:
            # 先檢測檔案編碼
            encoding = self.detect_encoding(file_path)
            
            # 使用檢測到的編碼讀取檔案
            subs = pysubs2.load(file_path, encoding=encoding)
            
            # 轉換為標準格式
            return self._convert_to_subtitle_events(subs)
            
        except UnicodeDecodeError:
            # 嘗試其他編碼
            for enc in self.common_encodings:
                try:
                    subs = pysubs2.load(file_path, encoding=enc)
                    return self._convert_to_subtitle_events(subs)
                except UnicodeDecodeError:
                    continue
            raise EncodingError(f"無法使用任何編碼讀取檔案: {file_path}")
        
        except Exception as e:
            raise FileAccessError(f"讀取字幕檔案時發生錯誤: {str(e)}")
    
    def write_subtitle(
        self, 
        events: List[SubtitleEvent], 
        output_directory: str,
        original_file: str,
        encoding: str = 'utf-8'
    ):
        """寫入字幕檔案
        
        Args:
            events: 要寫入的字幕事件列表
            output_directory: 輸出目錄路徑
            original_file: 原始字幕檔案路徑
            encoding: 輸出檔案編碼，預設 utf-8
        """
        try:
            # 檢查輸出目錄是否存在
            output_dir = Path(output_directory)
            if not output_dir.exists():
                raise FileAccessError(f"輸出目錄不存在: {output_directory}")
                
            # 檢查原始檔案是否存在
            original_path = Path(original_file)
            if not original_path.exists():
                raise FileAccessError(f"原始檔案不存在: {original_file}")
                
            # 生成輸出檔案路徑
            output_filename = f"{original_path.stem}_translated{original_path.suffix}"
            output_path = output_dir / output_filename
            
            # 讀取原始檔案保留格式和樣式
            subs = pysubs2.load(original_file)
            
            # 更新翻譯內容
            self._update_subtitle_events(subs, events)
            
            # 儲存檔案
            subs.save(str(output_path), encoding=encoding)
            
        except SubtitleHandlerError:
            # 重新拋出已經自定義的錯誤
            raise
        except Exception as e:
            raise FileAccessError(f"寫入字幕檔案時發生錯誤: {str(e)}")
    
    def validate_file(self, file_path: str) -> bool:
        """驗證檔案格式"""
        try:
            path = Path(file_path)
            return path.exists() and path.suffix.lower() in self.supported_formats
        except Exception:
            return False
            
    def _convert_to_subtitle_events(self, subs: pysubs2.SSAFile) -> List[SubtitleEvent]:
        """將 pysubs2 格式轉換為標準格式"""
        events = []
        for i, event in enumerate(subs):
            events.append(SubtitleEvent(
                index=i + 1,
                start=event.start,
                end=event.end,
                text=event.text
            ))

        return events
        
    def _update_subtitle_events(self, subs: pysubs2.SSAFile, events: List[SubtitleEvent]):
        """更新現有字幕檔案的內容"""
        for event, new_event in zip(subs.events, events):
            if new_event.translation_text:  # 只更新有翻譯內容的部分
                event.text = new_event.translation_text
                
if __name__ == "__main__":
    # path = ""
    # handler = SubtitleHandler()
    # events = handler.read_subtitle(path)
    # print("\n"*2)
    # print(events)
    pass