# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'llm_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, ComboBox, DoubleSpinBox, EditableComboBox,
    LineEdit, PasswordLineEdit, PushButton, TitleLabel)

class Ui_LLMSettings(object):
    def setupUi(self, LLMSettings):
        if not LLMSettings.objectName():
            LLMSettings.setObjectName(u"LLMSettings")
        LLMSettings.resize(992, 655)
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(12)
        LLMSettings.setFont(font)
        self.verticalLayout = QVBoxLayout(LLMSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        self.formLayout.setVerticalSpacing(30)
        self.formLayout.setContentsMargins(12, 24, 24, 24)
        self.modelProviderLabel = BodyLabel(LLMSettings)
        self.modelProviderLabel.setObjectName(u"modelProviderLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.modelProviderLabel)

        self.modelProviderCombobox = ComboBox(LLMSettings)
        self.modelProviderCombobox.setObjectName(u"modelProviderCombobox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.modelProviderCombobox)

        self.modelChoosingLabel = BodyLabel(LLMSettings)
        self.modelChoosingLabel.setObjectName(u"modelChoosingLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.modelChoosingLabel)

        self.modelChoosingCombobox = EditableComboBox(LLMSettings)
        self.modelChoosingCombobox.setObjectName(u"modelChoosingCombobox")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.modelChoosingCombobox)

        self.modelTemperatureLabel = BodyLabel(LLMSettings)
        self.modelTemperatureLabel.setObjectName(u"modelTemperatureLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.modelTemperatureLabel)

        self.modelTemperatureSpinBox = DoubleSpinBox(LLMSettings)
        self.modelTemperatureSpinBox.setObjectName(u"modelTemperatureSpinBox")
        self.modelTemperatureSpinBox.setMaximum(1.000000000000000)
        self.modelTemperatureSpinBox.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.modelTemperatureSpinBox)

        self.LLMTestButton = PushButton(LLMSettings)
        self.LLMTestButton.setObjectName(u"LLMTestButton")
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(18)
        self.LLMTestButton.setFont(font1)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.LLMTestButton)

        self.APIKeyLabel = BodyLabel(LLMSettings)
        self.APIKeyLabel.setObjectName(u"APIKeyLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.APIKeyLabel)

        self.APIKeyLineEdit = PasswordLineEdit(LLMSettings)
        self.APIKeyLineEdit.setObjectName(u"APIKeyLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.APIKeyLineEdit)

        self.APIAdressLineEdit = LineEdit(LLMSettings)
        self.APIAdressLineEdit.setObjectName(u"APIAdressLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.APIAdressLineEdit)

        self.APIAdressLabel = BodyLabel(LLMSettings)
        self.APIAdressLabel.setObjectName(u"APIAdressLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.APIAdressLabel)

        self.label = TitleLabel(LLMSettings)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(0, QFormLayout.FieldRole, self.horizontalSpacer)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(LLMSettings)

        QMetaObject.connectSlotsByName(LLMSettings)
    # setupUi

    def retranslateUi(self, LLMSettings):
        LLMSettings.setWindowTitle(QCoreApplication.translate("LLMSettings", u"Form", None))
        self.modelProviderLabel.setText(QCoreApplication.translate("LLMSettings", u"\u6a21\u578b\u4f9b\u61c9\u5546", None))
        self.modelChoosingLabel.setText(QCoreApplication.translate("LLMSettings", u"\u9078\u64c7\u6a21\u578b", None))
        self.modelTemperatureLabel.setText(QCoreApplication.translate("LLMSettings", u"Temperature", None))
        self.LLMTestButton.setText(QCoreApplication.translate("LLMSettings", u"\u5132\u5b58\u4e26\u6e2c\u8a66", None))
        self.APIKeyLabel.setText(QCoreApplication.translate("LLMSettings", u"APIKEY", None))
        self.APIAdressLabel.setText(QCoreApplication.translate("LLMSettings", u"API \u4f4d\u5740", None))
        self.label.setText(QCoreApplication.translate("LLMSettings", u"\u6a21\u578b\u8a2d\u5b9a", None))
    # retranslateUi

