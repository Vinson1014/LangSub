# 這個檔案用於處理術語問題 被 main_ui.py 所調用

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
from services import SubtitleEvent, SubtitleHandler
from .exceptions import TerminologyError

@dataclass
class ContextInfo:
    """字幕上下文資訊"""
    subtitle_text: str    # 包含術語的字幕文本
    line_number: int     # 行號
    prev_context: str    # 前文
    next_context: str    # 後文

class TerminologyHandler:
    """術語處理器
    
    用於管理翻譯術語表和相關上下文資訊
    """
    
    def __init__(self):
        self.subtitle_handler = SubtitleHandler()        
        self.terminology_dict: Dict[str, str] = {}
        self.context_map: Dict[str, List[ContextInfo]] = {}
        self.subtitles = None
        self.source_file = None
    
    @classmethod
    async def create(
        cls,
        subtitles_file_path: Optional[Path] = None,
        output_dir_path: Optional[Path] = None
    ) -> 'TerminologyHandler':
        """異步工廠方法，用於創建 TerminologyHandler 實例"""
        handler = cls()
        if subtitles_file_path and output_dir_path:
            await handler.initialize(subtitles_file_path, output_dir_path)
        return handler
    
    async def initialize(
        self,
        subtitles_file_path: Path,
        output_dir_path: Path
    ) -> None:
        """異步初始化方法"""
        try:
            if subtitles_file_path.exists() and output_dir_path.exists():
                self.subtitle_file_path = subtitles_file_path
                self.output_dir_path = output_dir_path
                self.terminology_table_path = output_dir_path / f"{subtitles_file_path.stem}_terminology_table.json"
                
            self.subtitles = self.subtitle_handler.read_subtitle(str(subtitles_file_path))
            self.source_file = str(subtitles_file_path)
            
            # 如果術語表已存在 則直接讀取術語表
            if self.load_glossary():
                # 利用術語表建立context_map
                for term in self.terminology_dict.keys():
                    self.context_map[term] = self._extract_context(term, self.subtitles)
                return
            keyword_path = output_dir_path / f"{subtitles_file_path.stem}_keywords.json"
            if keyword_path.exists():
                await self.load_from_keywords(str(keyword_path))
            else:
                raise FileNotFoundError(f"找不到關鍵字檔案：{keyword_path}")
                
        except Exception as e:
            raise TerminologyError(f"術語處理器初始化失敗：{str(e)}")
 
    async def load_from_keywords(self, keyword_json_path: str) -> None:
        """從關鍵字提取結果載入初始術語表
        
        Args:
            keyword_json_path: 關鍵字 JSON 檔案路徑
        """
        with open(keyword_json_path, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
        
        for keyword in keywords:
            self.terminology_dict[keyword['name']] = ""  # 初始翻譯為空
            if self.subtitles:
                self.context_map[keyword['name']] = self._extract_context(
                    keyword['name'],
                    self.subtitles
                )
    
    def _extract_context(
        self,
        term: str,
        subtitles: List[SubtitleEvent],
        context_length: int = 2
    ) -> List[ContextInfo]:
        """從字幕中提取術語的上下文
        
        Args:
            term: 要搜尋的術語
            subtitles: 字幕事件列表
            context_length: 上下文長度（前後各取幾行）
        
        Returns:
            List[ContextInfo]: 包含術語的字幕及其上下文資訊列表
        """
        results: List[ContextInfo] = []
        seen_indices = set()  # 用來追蹤已處理的字幕索引
        
        for index, subtitle in enumerate(subtitles):
            if index in seen_indices:
                continue
            
            if term in subtitle.text:
                # 確定上下文範圍
                start_index = max(index - context_length, 0)
                end_index = min(index + context_length + 1, len(subtitles))
                
                # 檢查後文是否也包含關鍵字，如果有則擴展範圍
                if any(term in s.text for s in subtitles[index+1:index+1 + context_length*2]):
                    end_index = min(end_index + 1 + context_length*2, len(subtitles))
                
                # 準備上下文
                prev_context = "\n".join(s.text for s in subtitles[start_index:index])
                next_context = "\n".join(s.text for s in subtitles[index+1:end_index])
                
                # 創建 ContextInfo
                context_info = ContextInfo(
                    subtitle_text=subtitle.text,
                    line_number=subtitle.index,
                    prev_context=prev_context,
                    next_context=next_context
                )
                
                results.append(context_info)
                seen_indices.update(range(start_index, end_index))
        
        return results
    
    # 術語操作方法
    def get_term_context(self, term: str) -> List[ContextInfo]:
        """獲取術語的上下文"""
        return self.context_map.get(term, [])
    
    def update_translation(self, term: str, translation: str) -> None:
        """更新術語翻譯"""
        self.terminology_dict[term] = translation
        self.save_glossary(str(self.terminology_table_path))
    
    def get_all_terms(self) -> Dict[str, str]:
        """獲取所有術語和翻譯"""
        return self.terminology_dict.copy()
    
    # 檔案操作方法
    def save_glossary(self, path: str) -> None:
        """儲存術語表"""
        data = {
            "terminology": self.terminology_dict,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "source_file": self.source_file
            }
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_glossary(self) -> bool:
        """載入既有術語表"""
        if self.terminology_table_path.exists():
            path = str(self.terminology_table_path)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.terminology_dict = data["terminology"]
            return True
        else:
            return False
