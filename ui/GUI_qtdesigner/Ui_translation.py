# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'translation.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, ComboBox, IndeterminateProgressRing, LineEdit,
    ProgressBar, ProgressRing, PushButton, TableView,
    TableWidget, TextBrowser, TitleLabel, ToolButton)

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName(u"HomePage")
        HomePage.resize(973, 721)
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(12)
        HomePage.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(HomePage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.segmentedWidgetLayout = QFormLayout()
        self.segmentedWidgetLayout.setObjectName(u"segmentedWidgetLayout")
        self.segmentedWidgetLayout.setContentsMargins(52, -1, 52, -1)

        self.verticalLayout_2.addLayout(self.segmentedWidgetLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(HomePage)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.subtitlesSelectionPage = QWidget()
        self.subtitlesSelectionPage.setObjectName(u"subtitlesSelectionPage")
        self.horizontalLayout_3 = QHBoxLayout(self.subtitlesSelectionPage)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(12)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(20, 30, 20, 20)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 6, 12, 6)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.inputSubtitlesLabel = BodyLabel(self.subtitlesSelectionPage)
        self.inputSubtitlesLabel.setObjectName(u"inputSubtitlesLabel")
        self.inputSubtitlesLabel.setFont(font)
        self.inputSubtitlesLabel.setLocale(QLocale(QLocale.Chinese, QLocale.Taiwan))

        self.horizontalLayout.addWidget(self.inputSubtitlesLabel)

        self.inputFileLineEdit = LineEdit(self.subtitlesSelectionPage)
        self.inputFileLineEdit.setObjectName(u"inputFileLineEdit")

        self.horizontalLayout.addWidget(self.inputFileLineEdit)

        self.inputFileSelection = ToolButton(self.subtitlesSelectionPage)
        self.inputFileSelection.setObjectName(u"inputFileSelection")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.inputFileSelection.setIcon(icon)

        self.horizontalLayout.addWidget(self.inputFileSelection)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 9)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.outputPathLabel = BodyLabel(self.subtitlesSelectionPage)
        self.outputPathLabel.setObjectName(u"outputPathLabel")
        self.outputPathLabel.setFont(font)

        self.horizontalLayout_4.addWidget(self.outputPathLabel)

        self.outputPathLineEdit = LineEdit(self.subtitlesSelectionPage)
        self.outputPathLineEdit.setObjectName(u"outputPathLineEdit")

        self.horizontalLayout_4.addWidget(self.outputPathLineEdit)

        self.outputPathSelection = ToolButton(self.subtitlesSelectionPage)
        self.outputPathSelection.setObjectName(u"outputPathSelection")
        self.outputPathSelection.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.outputPathSelection)

        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 9)
        self.horizontalLayout_4.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.outputModeLabel = BodyLabel(self.subtitlesSelectionPage)
        self.outputModeLabel.setObjectName(u"outputModeLabel")
        self.outputModeLabel.setFont(font)

        self.horizontalLayout_6.addWidget(self.outputModeLabel)

        self.outputModeComboBox = ComboBox(self.subtitlesSelectionPage)
        self.outputModeComboBox.addItem("")
        self.outputModeComboBox.addItem("")
        self.outputModeComboBox.addItem("")
        self.outputModeComboBox.setObjectName(u"outputModeComboBox")
        self.outputModeComboBox.setFont(font)

        self.horizontalLayout_6.addWidget(self.outputModeComboBox)

        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 10)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.targetLanguageLabel = BodyLabel(self.subtitlesSelectionPage)
        self.targetLanguageLabel.setObjectName(u"targetLanguageLabel")

        self.horizontalLayout_7.addWidget(self.targetLanguageLabel)

        self.targetLanguageLineEdit = LineEdit(self.subtitlesSelectionPage)
        self.targetLanguageLineEdit.setObjectName(u"targetLanguageLineEdit")

        self.horizontalLayout_7.addWidget(self.targetLanguageLineEdit)

        self.line = QFrame(self.subtitlesSelectionPage)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_7.addWidget(self.line)

        self.regionLabel = BodyLabel(self.subtitlesSelectionPage)
        self.regionLabel.setObjectName(u"regionLabel")

        self.horizontalLayout_7.addWidget(self.regionLabel)

        self.regionLineEdit = LineEdit(self.subtitlesSelectionPage)
        self.regionLineEdit.setObjectName(u"regionLineEdit")

        self.horizontalLayout_7.addWidget(self.regionLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.progressRing = ProgressRing(self.subtitlesSelectionPage)
        self.progressRing.setObjectName(u"progressRing")
        self.progressRing.setValue(24)

        self.horizontalLayout_2.addWidget(self.progressRing)

        self.ExecutionButton = PushButton(self.subtitlesSelectionPage)
        self.ExecutionButton.setObjectName(u"ExecutionButton")
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setUnderline(False)
        self.ExecutionButton.setFont(font1)

        self.horizontalLayout_2.addWidget(self.ExecutionButton)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(2, 7)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout_2.setRowStretch(0, 5)

        self.horizontalLayout_3.addLayout(self.gridLayout_2)

        self.stackedWidget.addWidget(self.subtitlesSelectionPage)
        self.keywordEditPage = QWidget()
        self.keywordEditPage.setObjectName(u"keywordEditPage")
        self.verticalLayout_5 = QVBoxLayout(self.keywordEditPage)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.keywordTranslationTableLabel = TitleLabel(self.keywordEditPage)
        self.keywordTranslationTableLabel.setObjectName(u"keywordTranslationTableLabel")

        self.verticalLayout_5.addWidget(self.keywordTranslationTableLabel)

        self.keywordLineTableWidget = TableWidget(self.keywordEditPage)
        self.keywordLineTableWidget.setObjectName(u"keywordLineTableWidget")

        self.verticalLayout_5.addWidget(self.keywordLineTableWidget)

        self.subtitlesWithKeywordLabel = TitleLabel(self.keywordEditPage)
        self.subtitlesWithKeywordLabel.setObjectName(u"subtitlesWithKeywordLabel")

        self.verticalLayout_5.addWidget(self.subtitlesWithKeywordLabel)

        self.subtitlesWithKeywordTableView = TableView(self.keywordEditPage)
        self.subtitlesWithKeywordTableView.setObjectName(u"subtitlesWithKeywordTableView")

        self.verticalLayout_5.addWidget(self.subtitlesWithKeywordTableView)

        self.stackedWidget.addWidget(self.keywordEditPage)
        self.outputMonitorPage = QWidget()
        self.outputMonitorPage.setObjectName(u"outputMonitorPage")
        self.verticalLayout_4 = QVBoxLayout(self.outputMonitorPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(12, 18, 18, 12)
        self.outputMonitorTitle = TitleLabel(self.outputMonitorPage)
        self.outputMonitorTitle.setObjectName(u"outputMonitorTitle")
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(20)
        font2.setBold(True)
        font2.setKerning(False)
        self.outputMonitorTitle.setFont(font2)
        self.outputMonitorTitle.setMargin(0)

        self.verticalLayout_4.addWidget(self.outputMonitorTitle)

        self.horizontalSpacer_3 = QSpacerItem(4, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_4.addItem(self.horizontalSpacer_3)

        self.outputMonitorTextBrowser = TextBrowser(self.outputMonitorPage)
        self.outputMonitorTextBrowser.setObjectName(u"outputMonitorTextBrowser")
        self.outputMonitorTextBrowser.setFont(font)

        self.verticalLayout_4.addWidget(self.outputMonitorTextBrowser)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = BodyLabel(self.outputMonitorPage)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setMargin(0)

        self.horizontalLayout_5.addWidget(self.label)

        self.progressSpinner = IndeterminateProgressRing(self.outputMonitorPage)
        self.progressSpinner.setObjectName(u"progressSpinner")
        self.progressSpinner.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressSpinner)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.progressBar = ProgressBar(self.outputMonitorPage)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressBar)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.stackedWidget.addWidget(self.outputMonitorPage)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(HomePage)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        HomePage.setWindowTitle(QCoreApplication.translate("HomePage", u"Form", None))
        self.inputSubtitlesLabel.setText(QCoreApplication.translate("HomePage", u"\u8f38\u5165\u5b57\u5e55", None))
        self.inputFileSelection.setText("")
        self.outputPathLabel.setText(QCoreApplication.translate("HomePage", u"\u8f38\u51fa\u8def\u5f91", None))
        self.outputPathSelection.setText("")
        self.outputModeLabel.setText(QCoreApplication.translate("HomePage", u"\u8f38\u51fa\u6a21\u5f0f", None))
        self.outputModeComboBox.setItemText(0, QCoreApplication.translate("HomePage", u"\u95dc\u9375\u5b57\u63d0\u53d6", None))
        self.outputModeComboBox.setItemText(1, QCoreApplication.translate("HomePage", u"\u7cbe\u7d30\u7ffb\u8b6f", None))
        self.outputModeComboBox.setItemText(2, QCoreApplication.translate("HomePage", u"\u5feb\u901f\u7ffb\u8b6f", None))

        self.targetLanguageLabel.setText(QCoreApplication.translate("HomePage", u"\u76ee\u6a19\u8a9e\u8a00", None))
        self.regionLabel.setText(QCoreApplication.translate("HomePage", u"\u5340\u57df", None))
        self.regionLineEdit.setInputMask("")
        self.regionLineEdit.setText("")
        self.ExecutionButton.setText(QCoreApplication.translate("HomePage", u"\u57f7\u884c", None))
        self.keywordTranslationTableLabel.setText(QCoreApplication.translate("HomePage", u"\u7ffb\u8b6f\u5c0d\u7167\u8868", None))
        self.subtitlesWithKeywordLabel.setText(QCoreApplication.translate("HomePage", u"\u95dc\u806f\u5b57\u5e55", None))
        self.outputMonitorTitle.setText(QCoreApplication.translate("HomePage", u"\u8f38\u51fa\u76e3\u8996\u5668", None))
        self.label.setText(QCoreApplication.translate("HomePage", u"\u9032\u5ea6", None))
    # retranslateUi

