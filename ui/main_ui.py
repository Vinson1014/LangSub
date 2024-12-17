# coding:utf-8
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import TranslationConfig
from LS_types import TranslationCallback, TranslationMode, ProgressInfo, TranslationState, BatchResult
from LS_core.translator import SubtitleTranslator
from utils import TerminologyHandler
from ui import Ui_HomePage, Ui_LLMSettings
from constants import ResourcePaths

import asyncio
from qasync import QEventLoop, asyncSlot

import logging
from PySide6.QtCore import (Qt, QLocale, QTranslator, QCoreApplication)
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel,
                               QVBoxLayout, QPushButton, QFileDialog, QComboBox, QWidget, 
                               QSpacerItem, QSizePolicy, QTableWidgetItem, QHeaderView)
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, SegmentedWidget, OptionsSettingCard, HyperlinkCard, QConfig, ConfigItem, isDarkTheme, 
                            setTheme, Theme, setThemeColor, FluentIcon as FIF)
from qfluentwidgets import *
from enum import Enum
from qframelesswindow import FramelessWindow, StandardTitleBar


logging.basicConfig(level=logging.INFO)

class DictValidator(ConfigValidator):
    """驗證字典格式"""

    def validate(self, value):
        if isinstance(value, str):
            logging.debug(f"dict is valid: {value}")
            return True
        logging.debug(f"dict is not valid: {value}")
        return False

class DictSerializer(ConfigSerializer):
    """處理字典序列化"""

    def serialize(self, value):
        logging.debug(f"serializing \n {value}")
        logging.debug(f"serializing type: {type(value)}\n")
        return json.dumps(value)

    def deserialize(self, value):
        logging.debug(f"deserializing \n {value}")
        logging.debug(f"deserializing type: {type(value)}\n")
        return json.loads(value)
    
class LocaleSerializer(ConfigSerializer):
    def serialize(self, locale):
        logging.debug(f"serializing \n {locale}")
        logging.debug(f"serializing type: {type(locale)}\n")

        return {
            "language": locale.language().name,
            "territory": locale.territory().name
        }

    def deserialize(self, value):
        logging.debug(f"deserializing \n {value}")
        logging.debug(f"deserializing type: {type(value)}\n")
        
        language = getattr(QLocale, value["language"])
        territory = getattr(QLocale, value["territory"])
        
        return QLocale(language, territory)

class MyConfig(QConfig):
    """ Config of application """

    # Model provider & Model List
    llmProviders = ConfigItem(
        group = "LLM Settings", 
        name = "Model Providers", 
        default = {
            "OpenAI": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini", "o1-mini", "o1-preview"],
            "Google": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
            "Anthropic": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"],
            "OpenAI Compatible API": []
        },
        validator = DictValidator(),
    )
    
    APIKey = ConfigItem(
        group="LLM Settings", 
        name="API Key", 
        default={
            "OpenAI": "",
            "Google": "",
            "Anthropic": "",
            "OpenAI Compatible API": ""
        },
        validator = DictValidator(),
    )
    
    temperature = ConfigItem(
        group="LLM Settings", 
        name="Temperature", 
        default=0.3,
        validator = RangeValidator(0, 1)
    )
    
    # OpenAI Compatible API
    llmAPIAddress = ConfigItem(
        group="LLM Settings", 
        name="OpenAI Compatible API Address", 
        default=""        
    )
    
    # latest setting
    latestSetting = ConfigItem(
        group="LLM Settings", 
        name="Latest Setting", 
        default={
            "provider": "OpenAI",
            "model": "gpt-4o-mini"
        }
    )
    
    # App Language
    language = OptionsConfigItem(
        group="App Settings", 
        name="Language", 
        default=QLocale(QLocale.English, QLocale.AnyCountry),
        validator= OptionsValidator([QLocale(QLocale.Chinese, QLocale.China), QLocale(QLocale.Chinese, QLocale.Taiwan), QLocale(QLocale.English, QLocale.AnyCountry)]),
        serializer = LocaleSerializer()
    )
    

# 创建配置实例并使用配置文件来初始化它
cfg = MyConfig()
qconfig.load('config/config.json', cfg)       
        
class MainWindow(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # 設定flag
        self.output_path_fixed = False
        
        self.setupUi(self)
        
        # 設定字幕上下文表格
        self.context_model = QStandardItemModel()
        self.subtitlesWithKeywordTableView.setModel(self.context_model)
        
        #初始化進度條
        self.progressRing.setValue(0)
        self.progressBar.setValue(0)
        
        # 在LineEdit 中加入說明
        self.inputFileLineEdit.setPlaceholderText(self.tr("選擇字幕檔"))
        self.outputPathLineEdit.setPlaceholderText(self.tr("選擇目的地"))
        self.targetLanguageLineEdit.setPlaceholderText(self.tr("目標語言"))
        self.regionLineEdit.setPlaceholderText(self.tr("輸入您的區域資訊以提升翻譯品質"))
        
        # 建立SegmentedWidget 實體
        self.segmentedWidget = SegmentedWidget(self)
        # self.segmentedWidgetLayout.addWidget(self.segmentedWidget,0,Qt.AlignHCenter)
        self.segmentedWidgetLayout.addWidget(self.segmentedWidget)
        
        # 添加標籤頁面
        self.addSubInterface(self.subtitlesSelectionPage, 'subtitlesSelectionPage', self.tr('字幕選擇'))
        self.addSubInterface(self.keywordEditPage, 'keywordEditPage', self.tr('關鍵字編輯'))
        self.addSubInterface(self.outputMonitorPage, 'outputMonitorPage', self.tr('輸出監視器'))
        
        # 保存路徑和對應的原始文字，用於後續更新
        self.pages_info = [
            ('subtitlesSelectionPage', lambda: self.tr('字幕選擇')),
            ('keywordEditPage', lambda: self.tr('關鍵字編輯')),
            ('outputMonitorPage', lambda: self.tr('輸出監視器'))
        ]
                
        self.stackedWidget.currentChanged.connect(self.onCurrentChanged)
        self.stackedWidget.setCurrentWidget(self.subtitlesSelectionPage)
        self.segmentedWidget.setCurrentItem(self.subtitlesSelectionPage.objectName())
        
        # 設定按鈕行為
        self.inputFileSelection.clicked.connect(self.selectSubtitle)
        self.outputPathSelection.clicked.connect(self.selectDestination)
        self.ExecutionButton.clicked.connect(self.handle_translation)
        
        # 設定表格
        self.keywordLineTableWidget.setBorderVisible(True)
        self.keywordLineTableWidget.setBorderRadius(8)
        self.keywordLineTableWidget.setWordWrap(False)
        self.keywordLineTableWidget.setColumnCount(2)
        self.keywordLineTableWidget.setHorizontalHeaderLabels([self.tr("術語"), self.tr("翻譯")])
        
        self.subtitlesWithKeywordTableView.setBorderVisible(True)
        self.subtitlesWithKeywordTableView.setBorderRadius(8)
        self.subtitlesWithKeywordTableView.setWordWrap(False)
        
        # self.keywordLineTableWidget.cellClicked.connect(self.updateContext)
        self.keywordLineTableWidget.itemClicked.connect(self.updateContext)
        self.keywordLineTableWidget.cellChanged.connect(self.onTableChanged)

        
        
        # 使表格填滿寬度 並隨UI寬度自動調節
        self.keywordLineTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subtitlesWithKeywordTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 設定widget
        self.progressRing.setFixedSize(35, 35)
        self.progressRing.setVisible(False)
        
        self.progressSpinner.setFixedSize(20, 20)
        self.progressSpinner.setStrokeWidth(2)
        self.progressSpinner.setCustomBarColor(Qt.GlobalColor.gray, Qt.GlobalColor.white)
        self.progressSpinner.setVisible(False)        
        
        # 加入翻譯器實例
        self.translator = None
    
    def onTableChanged(self):
        """當用戶編輯表格時 更新術語表"""
        # 建立當前術語表(從表格讀取)
        terminology_dict = {}
        for i in range(self.keywordLineTableWidget.rowCount()):
            terminology_dict[self.keywordLineTableWidget.item(i, 0).text()] = self.keywordLineTableWidget.item(i, 1).text()
        
        # 更新terminology handler
        self.terminology_handler.terminology_dict = terminology_dict
        # 將結果儲存
        self.terminology_handler.save_glossary(str(self.terminology_handler.terminology_table_path))

    def updateContext(self, item):
        """當用戶點擊術語時 更新包含術語的字幕及其上下文"""
        # 清空現有內容
        self.context_model.removeRows(0, self.context_model.rowCount())
        
        row = self.keywordLineTableWidget.row(item)
        column = self.keywordLineTableWidget.column(item)
        # print(f"位置: Row {row}, Column {column}")
        # print(f"關鍵字: {self.keywordLineTableWidget.item(row, 0).text()}, 翻譯: {self.keywordLineTableWidget.item(row, 1).text()}")
        contexts = self.terminology_handler.get_term_context(self.keywordLineTableWidget.item(row, 0).text())

        # 添加新的內容
        for context in contexts:
            self.context_model.appendRow(QStandardItem(context.prev_context))
            self.context_model.appendRow(QStandardItem(context.subtitle_text))
            self.context_model.appendRow(QStandardItem(context.next_context))
            self.context_model.appendRow(QStandardItem("\n"))
        
    @asyncSlot()
    async def updateKeywordTable(self):

        # 讀取字幕檔案名稱
        subtitle_path = Path(self.inputFileLineEdit.text())
        output_path = Path(self.outputPathLineEdit.text())
        
        if not subtitle_path.exists():
            raise FileNotFoundError(f"字幕檔案不存在: {subtitle_path}")

        if not output_path.exists():
            raise FileNotFoundError(f"目的地不存在: {output_path}")
        
        # 建立terminology handler 實體
        self.terminology_handler = await TerminologyHandler.create(subtitles_file_path=subtitle_path, output_dir_path=output_path)
        
        keywords = self.terminology_handler.terminology_dict
        
        # 設定表格row數
        self.keywordLineTableWidget.setRowCount(len(keywords))

        # 暫時解除觸發更新
        self.keywordLineTableWidget.cellChanged.disconnect(self.onTableChanged)
        
        # 添加表格数据
        for i, keyword in enumerate(keywords):
            keys = list(keywords.keys())
            self.keywordLineTableWidget.setItem(i, 0, QTableWidgetItem(keys[i]))
            self.keywordLineTableWidget.setItem(i, 1, QTableWidgetItem(keywords[keys[i]]))

        # 重新啟用觸發更新  
        self.keywordLineTableWidget.cellChanged.connect(self.onTableChanged)

      
    def addSubInterface(self, widget: QWidget, objectName: str, text: str):
        widget.setObjectName(objectName)
        
        self.stackedWidget.addWidget(widget)
        
        self.segmentedWidget.addItem(
            routeKey=objectName, 
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )
        
    def onCurrentChanged(self, index):
        if index == 1: # 如果是關鍵字編輯頁面
            self.updateKeywordTable()
        widget = self.stackedWidget.widget(index)
        self.segmentedWidget.setCurrentItem(widget.objectName())
        
        
    def selectSubtitle(self):
        path, _ = QFileDialog.getOpenFileName(self, self.tr("選擇字幕檔"), "", "Subtitle Files (*.srt *.ass *.vtt)")
        if path:
            self.inputFileLineEdit.setText(f"{path}")
            # 預設目的地為字幕檔相同目錄
            if not self.output_path_fixed:
                self.outputPathLineEdit.setText(f"{path.rsplit('/', 1)[0]}")

    def selectDestination(self):
        path = QFileDialog.getExistingDirectory(self, self.tr("選擇目的地"))
        if path:
            self.outputPathLineEdit.setText(f"{path}")
            self.output_path_fixed = True

    class UICallback():
        """翻譯進度回調"""
        def __init__(self, window: 'MainWindow'):
            self.window = window
            
        def on_progress(self, progress: ProgressInfo):
            # 更新進度條和狀態
            self.window.progressBar.setValue(
                int(progress.current_line / progress.total_lines * 100)
            )
            self.window.progressRing.setValue(
                int(progress.current_line / progress.total_lines * 100)
            )
            
            
        def on_state_change(self, state: TranslationState):
            # 更新狀態顯示
            pass
            
        def on_error(self, error: Exception):
            # 顯示錯誤訊息
            InfoBar.error(
                title=self.window.tr("錯誤"),
                content=f"翻譯過程發生錯誤: {str(error)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=10000,
                parent=self
            )
            
        def on_batch_complete(self, batch_info: BatchResult):
            # 顯示批次完成訊息
            self.window.outputMonitorTextBrowser.append(f"\n----------\n{batch_info.llm_raw_output}\n----------\n")
    
    def initialize_translator(self):
        """初始化翻譯器"""
        # 直接使用全局 cfg 實例
        latest_setting = cfg.get(cfg.latestSetting)
        api_keys = cfg.get(cfg.APIKey)
        
        translation_config = TranslationConfig(
            provider=latest_setting["provider"],
            model=latest_setting["model"],
            api_key=api_keys[latest_setting["provider"]],
            temperature=cfg.get(cfg.temperature),
            api_base=cfg.get(cfg.llmAPIAddress) if latest_setting["provider"] == "OpenAI Compatible API" else None
        )
        
        self.translator = SubtitleTranslator(translation_config)
        self.translator.set_progress_callback(self.UICallback(self))
        
    @asyncSlot()
    async def handle_translation(self):
        """處理翻譯按鈕點擊"""
        try:
            self.ExecutionButton.setEnabled(False)  # 禁用按鈕防止重複點擊
            self.progressRing.setVisible(True)  # 顯示進度條
            self.progressSpinner.setVisible(True)  # 顯示進度條
            await self.startTranslation()
        except Exception as e:
            InfoBar.error(
                title=self.tr("翻譯錯誤"),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=10000,
                parent=self
            )
        finally:
            self.ExecutionButton.setEnabled(True)  # 重新啟用按鈕
            self.progressRing.setVisible(False)  # 隱藏進度條
            self.progressSpinner.setVisible(False)  # 隱藏進度條
    
    async def startTranslation(self):
        """開始翻譯流程"""
        try:
            # 檢查輸入
            if not self.inputFileLineEdit.text():
                raise ValueError(self.tr("請選擇輸入檔案"))
            if not self.outputPathLineEdit.text():
                raise ValueError(self.tr("請選擇輸出路徑"))
            
            # 初始化翻譯器
            self.initialize_translator()
            
            # 根據UI回傳運作模式
            output_mode = self.outputModeComboBox.currentIndex()
            if output_mode == 0:
                output_mode = TranslationMode.KEYWORDS
            elif output_mode == 1:
                output_mode = TranslationMode.DETAILED
            elif output_mode == 2:
                output_mode = TranslationMode.QUICK
            
            # 執行翻譯
            await self.translator.process_by_mode(
                input_path=self.inputFileLineEdit.text(),
                output_directory=self.outputPathLineEdit.text(),
                mode=output_mode,
                target_language=self.targetLanguageLineEdit.text(),
                region=self.regionLineEdit.text()
            )
            
        except Exception as e:
            InfoBar.error(
                title=self.tr("翻譯錯誤"),
                content=str(e),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=10000,
                parent=self
            )
            
    def update_custom_translations(self):
        self.inputFileLineEdit.setPlaceholderText(self.tr("請選擇字幕檔"))
        self.outputPathLineEdit.setPlaceholderText(self.tr("請選擇目的地"))
        self.targetLanguageLineEdit.setPlaceholderText(self.tr("目標語言"))
        self.regionLineEdit.setPlaceholderText(self.tr("輸入您的區域資訊以提升翻譯品質"))
        # 更新 segmentedWidget 中的文字
        for route_key, get_text in self.pages_info:
            self.segmentedWidget.setItemText(route_key, get_text())
        
        self.keywordLineTableWidget.setHorizontalHeaderLabels([self.tr("術語"), self.tr("翻譯")])


class LLMSettingPage(QWidget, Ui_LLMSettings):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        
        self.APIAdressLineEdit.setVisible(False)
        self.APIAdressLabel.setVisible(False)
        
        # 讀取config 設定
        self.load_config()
        
        self.modelProviderCombobox.addItems(self.providers.keys())
        
        # init temperature
        self.modelTemperatureSpinBox.setValue(self.temperature)
        
        # init Latest Setting
        self.modelProviderCombobox.setCurrentText(self.latest_setting["provider"])
        
        # 初始顯示 Model ComboBox 的內容
        self.update_model_combo()
        
        # 連接信號與槽
        self.modelProviderCombobox.currentIndexChanged.connect(self.update_model_combo)
        # self.modelTemperatureSpinBox.valueChanged.connect(self.write_config)
        self.LLMTestButton.clicked.connect(self.write_config)     
  
    def load_config(self):
        logging.debug("load from config...")
        self.providers = cfg.get(cfg.llmProviders)
        self.APIKey = cfg.get(cfg.APIKey)
        self.temperature = cfg.get(cfg.temperature)
        self.APIAddress = cfg.get(cfg.llmAPIAddress)
        self.latest_setting = cfg.get(cfg.latestSetting)
        
        #debug message
        logging.debug(f"providers: \n{self.providers}")
        
        logging.debug(f"APIKey: \n{self.APIKey}")
        
        logging.debug(f"temperature: \n{self.temperature}")
        
        logging.debug(f"APIAddress: \n{self.APIAddress}")
        
        logging.debug(f"latest_setting: \n{self.latest_setting}")
        
    def update_model_combo(self):
        # 獲取當前選擇的 Provider
        current_provider = self.modelProviderCombobox.currentText() 
        # 刷新APIKey
        self.APIKeyLineEdit.setText(self.APIKey[current_provider])
        # 獲取對應的 Model 列表
        models = self.providers[current_provider]
        # 清空 Model ComboBox 並添加新的選項
        self.modelChoosingCombobox.clear()
        self.modelChoosingCombobox.addItems(models)
        
        # init latest setting
        if self.latest_setting["model"] in models:
            self.modelChoosingCombobox.setCurrentText(self.latest_setting["model"])
        
        # 根據選擇的 Provider 顯示或隱藏 API 地址輸入框
        if current_provider == "OpenAI Compatible API":
            self.APIAdressLabel.setVisible(True)
            self.APIAdressLineEdit.setVisible(True)
            self.APIAdressLineEdit.setText(self.APIAddress)
        else:
            self.APIAdressLabel.setVisible(False)
            self.APIAdressLineEdit.setVisible(False)
            
        self.write_config()
            
    def write_config(self):
        logging.debug("write_config to config...")
        
        # Model & Providers
        # 檢查model 是否已經存在list 中
        llm_providers = self.providers
        if self.modelChoosingCombobox.currentText() not in llm_providers[self.modelProviderCombobox.currentText()] and self.modelChoosingCombobox.currentText() != "":
            logging.debug(f"新增模型: {self.modelChoosingCombobox.currentText()} to {self.modelProviderCombobox.currentText()}")
            llm_providers[self.modelProviderCombobox.currentText()].append(self.modelChoosingCombobox.currentText())
        cfg.set(cfg.llmProviders, llm_providers)
        
        # APIKey
        if self.APIKeyLineEdit.text() != self.APIKey[self.modelProviderCombobox.currentText()]:
            self.APIKey[self.modelProviderCombobox.currentText()] = self.APIKeyLineEdit.text()
        cfg.set(cfg.APIKey, self.APIKey)
        
        # APIAddress
        if self.APIAdressLineEdit.text() != self.APIAddress and self.modelProviderCombobox.currentText() == "OpenAI Compatible API":
            self.APIAddress = self.APIAdressLineEdit.text()
        cfg.set(cfg.llmAPIAddress, self.APIAddress)
        
        # Temperature
        cfg.set(cfg.temperature, self.modelTemperatureSpinBox.value()) 
        
        # Latest Setting
        cfg.set(cfg.latestSetting, {
            "provider": self.modelProviderCombobox.currentText(),
            "model": self.modelChoosingCombobox.currentText()
        })
        
        cfg.save()
        self.load_config()

class AppSettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('appSettingsPage')
        
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """設置基本UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 24, 24, 24)
        layout.setAlignment(Qt.AlignTop)
        
        # 創建所有 widgets 並直接設置文字
        self.SettingTitle = TitleLabel(self.tr("應用程式設定"))
        
        # 所有 widgets 放到類屬性中，以便後續更新文字
        self.themeCard = OptionsSettingCard(
            qconfig.themeMode,
            FIF.BRUSH,
            self.tr("主題顏色"),
            self.tr("調整應用程式外觀"),
            texts=[self.tr("淺色"), self.tr("深色"), self.tr("跟隨系統設定")]
        )
        
        self.languageCard = ComboBoxSettingCard(
            configItem=cfg.language,
            icon=FIF.LANGUAGE,
            title=self.tr("語言"),
            content=self.tr("選擇應用程式的語言"),
            texts=["中文(简体)", "中文(繁體)", "English"]
        )

        self.linkCard = HyperlinkCard(
            url="https://github.com/Vinson1014/LangSub",
            text=self.tr("打開幫助文件"),
            icon=FIF.HELP,
            title=self.tr("幫助"),
            content=self.tr("了解如何使用應用程式的詳細指南")
        )
        
        # 添加到布局
        layout.addWidget(self.SettingTitle, alignment=Qt.AlignTop)
        layout.addWidget(self.themeCard, alignment=Qt.AlignTop)
        layout.addWidget(self.languageCard, alignment=Qt.AlignTop)
        layout.addWidget(self.linkCard, alignment=Qt.AlignTop)
    
    def setup_connections(self):
        """設置信號連接"""
        self.themeCard.optionChanged.connect(self.toggle_theme)
                  
    def toggle_theme(self):
        current_theme = cfg.get(cfg.themeMode)
        setTheme(current_theme, save=True, lazy=True)
        
    def update_custom_translations(self):
        """更新設定頁面所有翻譯文字"""
        self.SettingTitle.setText(self.tr("應用程式設定"))
        # 更新主題卡片文字
        self.themeCard.card.titleLabel.setText(self.tr("主題顏色"))
        self.themeCard.card.contentLabel.setText(self.tr("調整應用程式外觀"))
        
        # 更新主題選項按鈕文字
        theme_buttons = self.themeCard.buttonGroup.buttons()
        theme_texts = [
            self.tr("淺色"),
            self.tr("深色"),
            self.tr("跟隨系統設定")
        ]
        for button, text in zip(theme_buttons, theme_texts):
            button.setText(text)
        
        # 更新語言卡片文字
        self.languageCard.titleLabel.setText(self.tr("語言"))
        self.languageCard.contentLabel.setText(self.tr("選擇應用程式的語言"))
        
        # 更新幫助卡片文字
        self.linkCard.titleLabel.setText(self.tr("幫助"))
        self.linkCard.contentLabel.setText(self.tr("了解如何使用應用程式的詳細指南"))
        self.linkCard.linkButton.setText(self.tr("打開幫助文件"))
        
class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        
        self.translator = QTranslator()

        # 初始化導航和內容區
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)
        
        # 定義各頁面
        self.mainPage = MainWindow(self)
        self.llmSettingsPage = LLMSettingPage(self)
        self.appSettingsPage = AppSettingsPage(self)

        # 設置導航和頁面
        self.initLayout()
        self.initNavigation()
        self.initWindow()
        
        self.languageChanged()
        self.appSettingsPage.themeCard.optionChanged.connect(self.setQss)
        cfg.language.valueChanged.connect(self.languageChanged)
        
    def update_custom_translations(self):
        self.mainPage.update_custom_translations()
        self.appSettingsPage.update_custom_translations()
        self.llmSettingsPage.retranslateUi(self)
        self.mainPage.retranslateUi(self)
        
        # 更新側邊導航欄
        self.navigationInterface.panel.items["HomePage"].widget.itemWidget.setText(self.tr("主頁面"))
        self.navigationInterface.panel.items["LLMSettings"].widget.itemWidget.setText(self.tr("模型設定"))
        self.navigationInterface.panel.items["appSettingsPage"].widget.itemWidget.setText(self.tr("應用程式設定"))
        
        self.setWindowTitle(self.tr("朗譯"))

    def languageChanged(self):
        """
        Handle language change event and load appropriate translation file.
        Uses QLocale to get language and territory information.
        """
        # Print current language and territory for debugging
        # print(f"languageChanged: {cfg.get(cfg.language).language().name},{cfg.get(cfg.language).territory().name}")
        
        # Get the current locale
        current_locale = cfg.get(cfg.language)
        
        # 如果是繁體中文，就不載入翻譯文件
        if current_locale.language().name == "Chinese" and current_locale.territory().name == "Taiwan":
            # 移除現有翻譯器
            if hasattr(self, 'translator'):
                _app = QApplication.instance()
                _app.removeTranslator(self.translator)
                self.update_custom_translations()
            return
        
        # Define translation file path pattern
        # Assuming translation files are in a 'ui/i18n' directory
        translation_file_pattern = "./ui/i18n/LangSub_{lang}_{territory}"

        # Map language and territory to file naming convention
        language_map = {
            "Chinese": "zh",
            "English": "en"
        }
        
        territory_map = {
            "Taiwan": "TW",
            "China": "CN",
            "UnitedStates": "US"
        }
        
        # Get language and territory codes
        lang_code = language_map.get(current_locale.language().name, "en")
        territory_code = territory_map.get(current_locale.territory().name, "US")
        
        # Construct the translation file path
        translation_path = translation_file_pattern.format(
            lang=lang_code,
            territory=territory_code
        )
        
        # Remove previous translator if exists
        if hasattr(self, 'translator'):
            _app = QApplication.instance()
            _app.removeTranslator(self.translator)
        
        # Load new translation
        self.translator = QTranslator()
        translation_loaded = self.translator.load(translation_path)
        
        if translation_loaded:
            _app = QApplication.instance()
            _app.installTranslator(self.translator)
            
            # Force update UI text
            self.llmSettingsPage.retranslateUi(self)
            self.mainPage.retranslateUi(self)
            self.update_custom_translations()
        else:
            print(f"Failed to load translation file: {translation_path}")
    
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):        
        # 左側導航
        self.addSubInterface(self.mainPage, FIF.HOME, self.tr("主頁面"), NavigationItemPosition.TOP)
        self.addSubInterface(self.llmSettingsPage, FIF.DEVELOPER_TOOLS, self.tr("模型設定"), NavigationItemPosition.TOP)
        self.addSubInterface(self.appSettingsPage, FIF.SETTING, self.tr("應用程式設定"), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle(self.tr("朗譯"))
        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        qss_path = ResourcePaths.QSS_DARK if color == 'dark' else ResourcePaths.QSS_LIGHT
        with open(qss_path, encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 設定異步事件循環
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    w = Window()
    w.show()

    with loop:
        loop.run_forever()



#TODO
# 當沒有keyword 資料時 彈訊息通知
# Error Message 調整, 使其能正確印出錯誤訊息
# 任務完成時要彈通知
