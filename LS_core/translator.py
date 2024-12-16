from enum import Enum
from typing import Optional, List, Dict
import time
import json
import asyncio
from pathlib import Path

from .state_manager import TranslationStateManager
from LS_types import TranslationState, TranslationProgress, TranslationCallback, ProgressInfo, BatchResult, TranslationMode
from services import LLMService, TranslationConfig, SubtitleHandler, SubtitleEvent
from utils import Logger, TranslationError, ConfigHandler
from strategies import TranslationStrategy, TranslationStrategyFactory

class SubtitleTranslator:
    """字幕翻譯協調器"""
    
    def __init__(self, translation_config: TranslationConfig):
        self.state_manager = TranslationStateManager()
        self.llm_service = LLMService(translation_config)
        self.subtitle_handler = SubtitleHandler()
        self.logger = Logger()
        self._progress_callback: Optional[TranslationCallback] = None
        
        # 初始化配置處理器
        self.config_handler = ConfigHandler()
        
        # 從配置檔讀取設定，若無則使用預設值
        self._batch_size = self.config_handler.get_value(
            "App Settings.Translation.batch_size", 
            default=3
        )
        self._context_window = self.config_handler.get_value(
            "App Settings.Translation.context_window_size", 
            default=2
        )
        
    def set_progress_callback(self, callback: TranslationCallback) -> None:
        """設置進度回調"""
        self._progress_callback = callback
        
    def _notify_progress(self, progress: ProgressInfo) -> None:
        """通知進度"""
        if self._progress_callback:
            self._progress_callback.on_progress(progress)
            
    def _notify_state_change(self, state: TranslationState) -> None:
        """通知狀態變更"""
        if self._progress_callback:
            self._progress_callback.on_state_change(state)
            
    def _notify_error(self, error: Exception) -> None:
        """通知錯誤"""
        if self._progress_callback:
            self._progress_callback.on_error(error)

    def _get_context_window(
        self,
        events: List[SubtitleEvent],
        current_index: int
    ) -> List[str]:
        """獲取上下文窗口"""
        start = max(0, current_index - self._context_window)
        end = min(len(events), current_index + self._batch_size + self._context_window)
        return [event.text for event in events[start:end]]
        
    def _prepare_batch(
        self,
        events: List[SubtitleEvent],
        start_index: int
    ) -> List[SubtitleEvent]:
        """準備批次處理的字幕"""
        end_index = min(start_index + self._batch_size, len(events))
        return events[start_index:end_index]

    async def process_by_mode(
        self,
        mode: TranslationMode,
        input_path: str,
        output_directory: str,
        target_language: str = "",
        region: str = ""
        ) -> None:
        """根據模式處理字幕

        Args:
            mode: 處理模式（翻譯或關鍵字提取）
            input_path: 輸入檔案路徑
            output_directory: 輸出目錄
            target_language: 目標語言（翻譯模式使用）
            region: 地區設定（翻譯模式使用）
        """
        try:            
            # 驗證輸入輸出路徑
            if not self.subtitle_handler.validate_file(input_path):
                raise TranslationError(f"不支援的檔案格式: {input_path}")
                
            output_dir = Path(output_directory)
            if not output_dir.exists():
                raise TranslationError(f"輸出目錄不存在: {output_directory}")
            
            # 測試terminology table 是否存在
            terminology_table_path = output_dir / f"{Path(input_path).stem}_terminology_table.json"
            if terminology_table_path.exists():
                # 讀取術語表
                with terminology_table_path.open("r", encoding="utf-8") as f:
                    terminology_table = json.load(f)
                    
            
            # 調整batch size if mode is keyword extraction(暫時使用此方式)
            if mode == TranslationMode.KEYWORDS:
                self._batch_size = 15
            
            # 建立對應策略
            strategy = TranslationStrategyFactory.create_strategy(mode)
            
            # 讀取字幕檔
            events = self.subtitle_handler.read_subtitle(input_path)
            total_lines = len(events)
            total_batches = (total_lines + self._batch_size - 1) // self._batch_size
            
            # 初始化狀態
            self.state_manager.start_translation(total_lines)
            self._notify_state_change(TranslationState.RUNNING)
            
            results = []
            current_index = 0
            
            while current_index < total_lines:
                # 檢查是否暫停
                while self.state_manager.state == TranslationState.PAUSED:
                    await asyncio.sleep(0.1)
                
                # 檢查是否取消
                if self.state_manager.state == TranslationState.IDLE:
                    return
                
                # 準備批次和上下文
                batch = self._prepare_batch(events, current_index)
                context = self._get_context_window(events, current_index)
                
                # 準備翻譯參考資料
                if mode != TranslationMode.KEYWORDS:
                    reference_info = self.generate_reference_info(batch, terminology_table["terminology"])
                else:
                    reference_info = None
                
                try:
                    # 執行策略處理
                    batch_results, raw_output = await strategy.process(
                        self.llm_service,
                        batch,
                        target_language,
                        region,
                        context,
                        reference_info
                    )
                    results.extend(batch_results)
                    
                    # 更新進度
                    self.logger.debug("更新當前進度")
                    current_batch = current_index // self._batch_size
                    progress = ProgressInfo(
                        current_batch=current_batch,
                        total_batches=total_batches,
                        current_line=current_index,
                        total_lines=total_lines,
                        current_text=batch[-1].text,
                        translated_text=batch[-1].translation_text if mode != TranslationMode.KEYWORDS else None
                    )
                    self._notify_progress(progress)

                    batch_result = BatchResult(
                        batch_index=current_batch,
                        results=batch_results,
                        llm_raw_output=raw_output
                    )
                    self._progress_callback.on_batch_complete(batch_result)
                    
                    
                    if mode != TranslationMode.KEYWORDS:
                        # 保存檢查點
                        self.state_manager.update_progress(
                            current_index + len(batch),
                            {i: e.translation_text for i, e in enumerate(batch, current_index)}
                        )
                        
                        # 更新翻譯結果到原始事件
                        # 使用 ID 對應更新翻譯結果
                        for result in batch_results:
                            # 找到對應的原始事件並更新                            
                            event = next(e for e in events if e.index == result['id'])
                            event.translation_text = result['translation_text']
                            
                except Exception as e:
                    self.logger.error(f"處理批次時發生錯誤: {str(e)}")
                    self._notify_error(e)
                    raise TranslationError(f"處理批次時發生錯誤: {str(e)}")
                
                current_index += len(batch)
            
            # 根據模式儲存結果
            if mode is TranslationMode.KEYWORDS:
                output_path = output_dir / f"{Path(input_path).stem}_keywords.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
            else:
                self.subtitle_handler.write_subtitle(
                    events=events,
                    output_directory=output_directory,
                    original_file=input_path
                )
            
            # 更新狀態
            progress = ProgressInfo(
                current_batch=current_batch,
                total_batches=total_batches,
                current_line=current_index,
                total_lines=total_lines,
                current_text=batch[-1].text,
                translated_text=batch[-1].translation_text if mode != TranslationMode.KEYWORDS else None
            )
            self._notify_progress(progress)
            self.state_manager.state = TranslationState.COMPLETED
            self._notify_state_change(TranslationState.COMPLETED)
            
        except Exception as e:
            self.state_manager.state = TranslationState.ERROR
            self._notify_state_change(TranslationState.ERROR)
            self.logger.error(f"處理過程發生錯誤: {str(e)}")
            self._notify_error(e)
            raise

    def generate_reference_info(self, batch: List[SubtitleEvent], terminology_table: Dict[str, str]) -> str:
        """回傳翻譯參考資訊
        
        從批次字幕中找出有包含在術語表的術語，並生成參考資訊
        
        Args:
            batch: 當前批次的字幕列表
            terminology_table: 術語對照表 {術語: 翻譯}
        
        Returns:
            str: 整理過的參考資訊字串，格式為:
                "在翻譯時請注意以下術語翻譯:\n
                    term1 -> translation1\n
                    term2 -> translation2\n
                    ..."
        """
        # 用於收集找到的術語
        found_terms = set()
        
        # 檢查每個字幕是否包含術語
        for event in batch:
            for term in terminology_table:
                if term in event.text:
                    found_terms.add(term)
        
        # 如果有找到術語，生成參考資訊
        if found_terms:
            reference_lines = ["Please pay attention to the following term translations when translating:"]
            for term in found_terms:
                reference_lines.append(f"{term} -> {terminology_table[term]}")
            return "\n".join(reference_lines)
        
        return ""  # 如果沒有找到相關術語，返回空字串
    
    def pause(self) -> None:
        """暫停翻譯"""
        if self.state_manager.state == TranslationState.RUNNING:
            self.state_manager.state = TranslationState.PAUSED
            self._notify_state_change(TranslationState.PAUSED)

    def resume(self) -> None:
        """繼續翻譯"""
        if self.state_manager.state == TranslationState.PAUSED:
            self.state_manager.state = TranslationState.RUNNING
            self._notify_state_change(TranslationState.RUNNING)

    def cancel(self) -> None:
        """取消翻譯"""
        self.state_manager.state = TranslationState.IDLE
        self._notify_state_change(TranslationState.IDLE)

    def get_progress(self) -> Optional[ProgressInfo]:
        """獲取當前進度"""
        return self.state_manager.get_progress()