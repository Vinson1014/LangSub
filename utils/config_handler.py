import json
from pathlib import Path
from typing import Any, Dict, Optional
from .exceptions import ConfigError

class ConfigHandler:
    """設定檔處理器"""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = Path(config_path)
        self.default_config = {
            "App Settings": {
                "Translation": {
                    "batch_size": 3,
                    "retry_limit": 4,
                    "checkpoint_interval": 10,
                    "temp_directory": "temp",
                    "log_directory": "logs"
                }
            }
        }
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """載入設定檔"""
        if not self.config_path.exists():
            self.config = self.default_config
            self._save_config()
            return
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self._ensure_config_structure()
        except json.JSONDecodeError as e:
            raise ConfigError(f"設定檔格式錯誤: {str(e)}")
        except Exception as e:
            raise ConfigError(f"載入設定檔時發生錯誤: {str(e)}")

    def _ensure_config_structure(self) -> None:
        """確保配置結構完整"""
        self._merge_configs(self.config, self.default_config)
        self._save_config()

    def _merge_configs(self, target: Dict, source: Dict) -> None:
        """遞迴合併配置"""
        for key, value in source.items():
            if key not in target:
                target[key] = value
            elif isinstance(value, dict):
                if not isinstance(target[key], dict):
                    target[key] = value
                else:
                    self._merge_configs(target[key], value)
    
    def _save_config(self) -> None:
        """儲存設定檔"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ConfigError(f"儲存設定檔時發生錯誤: {str(e)}")
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """獲取設定值"""
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            if default is not None:
                return default
            raise ConfigError(f"設定項不存在: {key}")
    
    def validate_config(self) -> None:
        """驗證必要設定"""
        required_keys = [
            'LLM Settings.API Key',
            'LLM Settings.Latest Setting.provider',
            'LLM Settings.Latest Setting.model',
            'App Settings.Translation'
        ]
        
        for key in required_keys:
            if self.get_value(key, None) is None:
                raise ConfigError(f"缺少必要設定: {key}")
    
    def update_value(self, key: str, value: Any) -> None:
        """更新設定值"""
        try:
            keys = key.split('.')
            target = self.config
            for k in keys[:-1]:
                target = target[k]
            target[keys[-1]] = value
            self._save_config()
        except Exception as e:
            raise ConfigError(f"更新設定時發生錯誤: {str(e)}")