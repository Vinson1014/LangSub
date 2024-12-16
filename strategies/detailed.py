# strategies/detailed.py

from .base import ProcessResult
from typing import List, Optional
from services import LLMService, SubtitleEvent
from prompts import TranslationPrompts
from services.retry import with_retry, RetryStrategy
from utils import LLMOutputError

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END


class DetailedTranslationStrategy:
    """詳細翻譯策略實現"""

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
        target_language: str,
        region: str,
        context: Optional[List[str]] = None,
        reference_info: Optional[str] = None,
        retry_times: int = 0,
        last_output: Optional[str] = None
    ) -> ProcessResult:
        """執行詳細翻譯
        
        使用 LangGraph 進行自我優化的翻譯流程
        """
        
        class TranslationState(TypedDict):
            target_language: str
            region: str
            context: Optional[List[str]]
            reference_info: Optional[str]
            subtitles: List[SubtitleEvent]
            initial_translation: Optional[str]
            llm_reflection: Optional[str]
            final_translation: Optional[List[dict]]
            
     
        async def initial_translate(state: TranslationState) -> TranslationState:
            system_prompt = TranslationPrompts.get_translation_prompt(
                target_language=state["target_language"],
                region=state["region"]
            )
            
            context_prompt = TranslationPrompts.get_context_input_prompt()
            
            context_text = "\n".join(state["context"]) if state["context"] else ""
            subtitles_yaml = "\n".join([f"- id: {subtitle.index}\n  text: \"{subtitle.text}\"" for subtitle in state["subtitles"]])
            
            response = await llm_service.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=context_prompt.format(
                    reference=state["reference_info"] or "",
                    context=context_text,
                    input=subtitles_yaml
                ))   
            ])
            translation = llm_service.extract_yaml(response)
            state["initial_translation"] = translation
            
            return state
        
        async def reflection(state: TranslationState) -> TranslationState:
            system_prompt = TranslationPrompts.get_reflection_prompt(
                target_language=state["target_language"],
                region=state["region"],
                initial_translation=state["initial_translation"],
                reference_info=state["reference_info"] or "",
            )
            
            response = await llm_service.llm.ainvoke([
                SystemMessage(content=system_prompt),
            ])
            
            reflection = response.content
            state["llm_reflection"] = reflection
            
            return state
        
        async def final_translate(state: TranslationState) -> TranslationState:
            system_prompt = TranslationPrompts.get_final_translation_system_prompt(
                target_language=state["target_language"]
            )
            
            context_prompt = TranslationPrompts.get_final_translation_prompt(
                initial_translation=state["initial_translation"],
                reflection=state["llm_reflection"]
            )
            
            response = await llm_service.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=context_prompt)
            ])
            
            translation = llm_service.extract_yaml(response)
            state["final_translation"] = llm_service.convert2json(translation)
            
            return state
        
        builder = StateGraph(TranslationState)
        
        builder.add_node("initial_translate", initial_translate)
        builder.add_node("reflection", reflection)
        builder.add_node("final_translate", final_translate)
        
        builder.add_edge(START, "initial_translate")
        builder.add_edge("initial_translate", "reflection")
        builder.add_edge("reflection", "final_translate")
        builder.add_edge("final_translate", END)
        
        graph = builder.compile()
        
        translation_state = TranslationState(
        target_language=target_language,
        region=region,
        context=context,
        reference_info=reference_info,
        subtitles=subtitles,
        initial_translation=None,
        llm_reflection=None,
        final_translation=None
        )
    
        result = await graph.ainvoke(translation_state)
        
        _initial_translation = result["initial_translation"]
        _reflection = result["llm_reflection"]
        _final_translation = llm_service.convert2yaml(result["final_translation"])
        
        llm_raw_output =f"initial_translation:\n{_initial_translation}\
        \n\nreflection:\n{_reflection}\
        \nfinal_translation:\n{_final_translation}"

        
        return result["final_translation"], llm_raw_output