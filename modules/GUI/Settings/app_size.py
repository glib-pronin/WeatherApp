from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt, pyqtSignal
from .settings_button import SettingsButton
from ...Tools import get_json

class AppSizeWidget(QWidget):
    dataChangedSignal = pyqtSignal(object)

    def __init__(self, height, lang, lang_dict):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("settingsMainContent")
        self.setFixedHeight(height)
        self.main_window_size = get_json("config.json")["main_window_size"]
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(24, 0, 0, 0)
        # Надпис
        self.title = QLabel(text=lang_dict[lang]["app_size_title"])
        self.title.setObjectName("settingsSectionContentTitle")
        self.main_layout.addWidget(self.title)
        # Радіокнопки з розмірами екрану, група для спільного керування
        self.rdb_layout = QVBoxLayout()
        self.rdb_layout.setSpacing(17)
        self.rdb_group = QButtonGroup(self)
        self.size1_rdb = QRadioButton(text="1200x800")
        self.size2_rdb = QRadioButton(text="1440x1024")
        self.size3_rdb = QRadioButton(text="1512x982")
        self.size4_rdb = QRadioButton(text="1728x1117")
        for size_rdb in (self.size1_rdb, self.size2_rdb, self.size3_rdb, self.size4_rdb):
            self.rdb_layout.addWidget(size_rdb)
            self.rdb_group.addButton(size_rdb)
            if size_rdb.text() == self.main_window_size:
                size_rdb.setChecked(True)
        self.main_layout.addLayout(self.rdb_layout)
        self.save_btn = SettingsButton(self.main_layout, 105, 38)
        self.save_btn.setText(lang_dict[lang]["save_btn_caption"])
        self.save_btn.clicked.connect(self.save_handler)
        self.rdb_group.buttonClicked.connect(self.save_btn.enable_btn)

    def save_handler(self):
        checked_btn = self.rdb_group.checkedButton()
        self.save_btn.disable_btn()
        self.dataChangedSignal.emit({"main_window_size": checked_btn.text()})
