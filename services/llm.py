# services/translation.py

from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from prompts.translation_prompts import TranslationPrompts
import yaml
import re

@dataclass
class TranslationConfig:
    provider: str
    model: str
    api_key: str
    temperature: float = 0.3
    api_base: Optional[str] = None

class LLMService:
    """翻譯服務的核心類"""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.llm = self._initialize_llm()
        self._progress_callback = None
        
    def _initialize_llm(self):
        """初始化 LLM"""
        if self.config.provider.lower() == "openai" or self.config.provider.lower() == "openai compatible api":
            return ChatOpenAI(
                model=self.config.model,
                temperature=self.config.temperature,
                api_key=self.config.api_key,
                base_url=self.config.api_base
            )
        elif self.config.provider.lower() == "anthropic":
            return ChatAnthropic(
                model=self.config.model,
                temperature=self.config.temperature,
                anthropic_api_key=self.config.api_key
            )
        elif self.config.provider.lower() == "google":
            return ChatGoogleGenerativeAI(
                model=self.config.model,
                temperature=self.config.temperature,
                api_key=self.config.api_key
            )
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def set_progress_callback(self, callback):
        """設置進度回調函數"""
        self._progress_callback = callback
        
    def extract_yaml(self, message: AIMessage) -> str:
        """將輸出中的YAML 取出"""
        text = message.content
        pattern = r"\`\`\`yaml(.*?)\`\`\`"
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            return match.strip()
            
    def convert2yaml(self, input_list: list[dict]) -> str:
        """將dictionary 轉換為 YAML"""
        return yaml.dump(input_list, allow_unicode=True)
        
    def convert2json(self, input_str: str) -> list[dict]:
        """將YAML 轉換為 dictionary"""
        return yaml.safe_load(input_str)



if __name__ == "__main__":
    pass
    