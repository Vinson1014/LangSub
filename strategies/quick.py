# strategies/quick.py

from .base import ProcessResult
from typing import List, Optional
from services import LLMService, SubtitleEvent
from prompts import TranslationPrompts
from services.retry import with_retry, RetryStrategy
from utils import LLMOutputError

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

class QuickTranslationStrategy:
    """快速翻譯策略實現"""

    @with_retry(RetryStrategy(
            max_attempts=4,
            initial_delay=1.0,
            max_delay=10.0,
            backoff_factor=2.0,
            errors=(Exception,)  # 可以根據需要指定具體的錯誤類型
        ))
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
        """執行快速翻譯
        
        直接使用 LLM 服務進行翻譯，不進行額外的優化或處理
        """
        # 建立提示模板
        system_prompt = TranslationPrompts.get_translation_prompt(
            target_language=target_language,
            region=region
        )
        
        context_prompt = TranslationPrompts.get_context_input_prompt()
        
        # 準備上下文
        context_text = "\n".join(context) if context else ""
        subtitles_yaml = self._subtitles_extraction(subtitles)
        
        # 執行翻譯
        response = await llm_service.llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=context_prompt.format(
                reference=reference_info or "",
                context=context_text,
                input=subtitles_yaml
            ))
        ])
        
        # 處理回應
        try:
            yaml_content = llm_service.extract_yaml(response)
            result = llm_service.convert2json(yaml_content)
            
            # 包含解析輸出:result 及LLM原始輸出:response
            return result, response.content
        
        except Exception as e:
            raise LLMOutputError(
                str(e),
                response.content
            )
    
    def _subtitles_extraction(self, subtitles: List[SubtitleEvent]) -> str:
        """將字幕內容提取出來並轉為YAML格式
        
        Args:
            subtitles: 字幕事件列表
            
        Returns:
            YAML 格式的字串，包含 id 和原文文本
        """
        # 建立列表來存儲每個事件的 YAML 格式
        yaml_entries = []
        
        # 處理每個字幕事件
        for subtitle in subtitles:
            yaml_entry = f"- id: {subtitle.index}\n  text: \"{subtitle.text}\""
            yaml_entries.append(yaml_entry)
        
        # 將所有條目用換行符連接
        return "\n".join(yaml_entries)