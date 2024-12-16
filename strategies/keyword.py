# strategies/keyword.py

from .base import ProcessResult
from typing import List, Optional
from services import LLMService, SubtitleEvent
from prompts import TranslationPrompts
from services.retry import with_retry, RetryStrategy
from utils import LLMOutputError

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

class KeywordExtractionStrategy:
    """關鍵字提取策略實現"""
        
    @with_retry(RetryStrategy(
            max_attempts=4,
            initial_delay=1.0,
            max_delay=10.0,
            backoff_factor=2.0,
            errors=(Exception,)
        ))
    async def process(
        self,
        llm_service: LLMService,
        subtitles: List[SubtitleEvent],
        target_language: str = "",            #為保持介面一致 值為空
        region: str = "",                     #為保持介面一致 值為空
        context: Optional[List[str]] = None,  #為保持介面一致 值為空
        reference_info: Optional[str] = None, #為保持介面一致 值為空
        retry_times: int = 0,
        last_output: Optional[str] = None
    ) -> ProcessResult:
        # 根據重試次數取得對應的 prompt
        system_prompt = self._get_prompt_by_retry(retry_times, last_output)
        
        # 準備 messages
        messages = [SystemMessage(content=system_prompt)]
        if retry_times < 2:  # 只有在非修復模式時才需要加入字幕內容
            messages.append(HumanMessage(
                content="\n".join(subtitle.text for subtitle in subtitles)
            ))
        
        # LLM 調用
        response = await llm_service.llm.ainvoke(messages)
        
        # 解析結果
        try:
            yaml_content = llm_service.extract_yaml(response)
            result = llm_service.convert2json(yaml_content)
            return result, response.content
        except Exception as e:
            raise LLMOutputError(str(e), response.content)

    def _get_prompt_by_retry(self, retry_times: int, last_output: Optional[str]) -> str:
        """根據重試次數取得對應的 prompt"""
        if retry_times == 0:
            return TranslationPrompts.get_keyword_extraction_prompt()
        elif retry_times < 2:
            base_prompt = TranslationPrompts.get_keyword_extraction_prompt()
            retry_prompt = TranslationPrompts.get_retry_prompt()
            return f"{base_prompt}\n{retry_prompt.format(retry_times=retry_times)}"
        else:
            return TranslationPrompts.get_repair_prompt(original_output=last_output)