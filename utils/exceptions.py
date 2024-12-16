class SubtitleTranslatorError(Exception):
    """字幕翻譯器基礎異常類別"""
    pass

class TranslationError(SubtitleTranslatorError):
    """翻譯過程錯誤"""
    pass

class FileError(SubtitleTranslatorError):
    """檔案處理相關錯誤"""
    pass

class EncodingError(FileError):
    """編碼相關錯誤"""
    pass

class ConfigError(SubtitleTranslatorError):
    """設定相關錯誤"""
    pass

class APIError(TranslationError):
    """API 呼叫相關錯誤"""
    def __init__(self, message: str, provider: str, status_code: int = None):
        self.provider = provider
        self.status_code = status_code
        super().__init__(f"{provider} API 錯誤: {message} (狀態碼: {status_code})")

class ValidationError(SubtitleTranslatorError):
    """驗證相關錯誤"""
    pass

class LLMOutputError(Exception):
    """用於攜帶 LLM 輸出的錯誤"""
    def __init__(self, message: str, output: str):
        super().__init__(message)
        self.output = output
        
class TerminologyError(SubtitleTranslatorError):
    """術語處理相關錯誤"""
    pass