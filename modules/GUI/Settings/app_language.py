from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from .settings_button import SettingsButton

class AppLangWidget(QWidget):
    COMBO_WIDTH = 239
    COMBO_HEIGHT = 32
    dataChangedSignal = pyqtSignal(object)

    def __init__(self, height, lang, lang_dict):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("settingsMainContent")
        self.setFixedHeight(height)
        self.lang = lang
        self.lang_dict = lang_dict
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(24, 0, 0, 0)
        # Надпис
        self.title = QLabel()
        self.title.setObjectName("settingsSectionContentTitle")
        self.main_layout.addWidget(self.title)
        # ВИпадаючий список з мовами
        self.combo_layout = QVBoxLayout()
        self.combo_layout.setSpacing(8)
        self.caption = QLabel()
        self.caption.setObjectName("settingsSectionContentCaption")
        self.combo_layout.addWidget(self.caption)
        self.combo_box = QComboBox()
        self.combo_box.setFixedSize(QSize(self.COMBO_WIDTH, self.COMBO_HEIGHT))
        self.combo_box.addItem("Українська", "ua")
        self.combo_box.addItem("English", "eng")
        self.index = self.combo_box.findData(self.lang) # Обираємо поточну мову
        self.combo_box.setCurrentIndex(self.index)
        self.combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_layout.addWidget(self.combo_box)
        self.main_layout.addLayout(self.combo_layout)
        # Кнопка збереження
        self.save_btn = SettingsButton(self.main_layout, 105, 38)
        self.save_btn.clicked.connect(self.save_handler)
        self.combo_box.currentIndexChanged.connect(self.save_btn.enable_btn)
        self.change_lang(self.lang)

    def save_handler(self):
        self.save_btn.disable_btn()
        self.dataChangedSignal.emit({"selected_lang": self.combo_box.currentData()})

    def change_lang(self, lang):
        self.lang = lang
        self.title.setText(self.lang_dict[self.lang]["app_lang_title"])
        self.caption.setText(self.lang_dict[self.lang]["app_lang_section"])
        self.save_btn.setText(self.lang_dict[self.lang]["save_btn_caption"])