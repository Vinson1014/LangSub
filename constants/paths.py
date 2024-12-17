import os
import sys

def get_app_root():
    """獲取應用程式根目錄"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ResourcePaths:
    """資源路徑配置"""
    APP_ROOT = get_app_root()
    RESOURCE_DIR = os.path.join(APP_ROOT, 'ui', 'resource')
    QSS_DARK = os.path.join(RESOURCE_DIR, 'dark', 'demo.qss')
    QSS_LIGHT = os.path.join(RESOURCE_DIR, 'light', 'demo.qss')