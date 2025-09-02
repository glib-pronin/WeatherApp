from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from .settings_button import SettingsButton
from .icons_list_card import IconsListCard

class IconsListWidget(QWidget):
    dataChangedSignal = pyqtSignal(object)

    def __init__(self, height, lang, lang_dict):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("settingsMainContent")
        self.setFixedHeight(height)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(24, 0, 0, 0)
        # Надпис 
        self.title = QLabel(text=lang_dict[lang]["icons_list_section"])
        self.title.setObjectName("settingsSectionContentTitle")
        self.main_layout.addWidget(self.title)
        # layout для списків картинок
        self.icons_list_layout = QVBoxLayout()
        self.icons_list_layout.setSpacing(0)
        self.main_layout.addLayout(self.icons_list_layout)
        # Кнопка збереження
        self.save_btn = SettingsButton(self.main_layout, 105, 38)
        self.save_btn.clicked.connect(self.save_handler)
        self.save_btn.setText(lang_dict[lang]["save_btn_caption"])
        # Сптсок картинок
        self.icons_list_cards = []
        self.icons_list_card1 = IconsListCard(self.icons_list_layout, "icons1", 1, self.icons_list_cards, self.save_btn.enable_btn)
        self.icons_list_card2 = IconsListCard(self.icons_list_layout, "icons2", 2, self.icons_list_cards, self.save_btn.enable_btn)
        self.icons_list_cards.extend([self.icons_list_card1, self.icons_list_card2])
        for icon_list_card in self.icons_list_cards:
            icon_list_card.title.setText(f"{lang_dict[lang]['icons_list_card_caption']}{icon_list_card.index}")

    def save_handler(self):
        for icon_list_card in self.icons_list_cards: # Знаходимо ораний список
            if icon_list_card.check_is_selected():
                self.save_btn.disable_btn()
                self.dataChangedSignal.emit({"selected_icons_folder": icon_list_card.folder})
                break