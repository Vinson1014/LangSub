# services/retry.py

import asyncio
from functools import wraps
import time
from typing import Callable, Any, Optional, Union
from utils import Logger, LLMOutputError

class RetryStrategy:
    """重試策略配置"""
    
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
        backoff_factor: float = 2.0,
        errors: tuple = (Exception,)
    ):
        """初始化重試策略
        
        Args:
            max_attempts: 最大嘗試次數
            initial_delay: 初始延遲時間（秒）
            max_delay: 最大延遲時間（秒）
            backoff_factor: 延遲時間增長因子
            errors: 需要重試的錯誤類型
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.errors = errors
        self.last_error = None  # 記錄上一次的錯誤
        self.last_output = None # 記錄上一次的輸出
        self.logger = Logger()

def with_retry(strategy: Optional[RetryStrategy] = None):
    """重試裝飾器
    
    Args:
        strategy: 重試策略，若為 None 則使用預設策略
    """
    if strategy is None:
        strategy = RetryStrategy()
        
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            delay = strategy.initial_delay
            last_exception = None
            
            for attempt in range(strategy.max_attempts):
                try:
                    if asyncio.iscoroutinefunction(func):
                        # 把重試次數和上一次輸出傳入函數
                        kwargs['retry_times'] = attempt
                        kwargs['last_output'] = strategy.last_output
                        return await func(*args, **kwargs)
                    return func(*args, **kwargs)
                except strategy.errors as e:
                    if isinstance(e, LLMOutputError):
                        strategy.last_output = e.output
                    strategy.last_error = e
                    
                    last_exception = e
                    if attempt == strategy.max_attempts - 1:
                        strategy.logger.error(
                            f"重試次數已達上限 ({strategy.max_attempts}次): {str(e)}"
                        )
                        raise
                    
                    strategy.logger.warning(
                        f"第 {attempt + 1} 次嘗試失敗，{delay} 秒後重試: {str(e)}"
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * strategy.backoff_factor, strategy.max_delay)
            
            raise last_exception
            
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            delay = strategy.initial_delay
            last_exception = None
            
            for attempt in range(strategy.max_attempts):
                try:
                    return func(*args, **kwargs)
                except strategy.errors as e:
                    last_exception = e
                    if attempt == strategy.max_attempts - 1:
                        strategy.logger.error(
                            f"重試次數已達上限 ({strategy.max_attempts}次): {str(e)}"
                        )
                        raise
                    
                    strategy.logger.warning(
                        f"第 {attempt + 1} 次嘗試失敗，{delay} 秒後重試: {str(e)}"
                    )
                    time.sleep(delay)
                    delay = min(delay * strategy.backoff_factor, strategy.max_delay)
            
            raise last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator