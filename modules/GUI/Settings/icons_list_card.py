from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from ..click_filter import ClickFilter
from ...Tools import get_image_path, get_json, refresh_widget

class IconsListCard(QWidget):
    CARD_WIDTH = 490
    CARD_HEIGHT = 136
    ICON_SIZE = 230
    ICON_LABEL_SIZE = 74

    def __init__(self, parent, folder, index, icons_list_cards, click_callback):
        super().__init__()
        parent.addWidget(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.folder = folder
        self.index = index
        self.selected_folder = get_json("config.json")["selected_icons_folder"]
        self.setObjectName("selectedIconListCard" if self.selected_folder == self.folder else "")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.icons_list_cards = icons_list_cards
        self.click_callback = click_callback
        self.click_filter = ClickFilter(self.click_handler)
        self.installEventFilter(self.click_filter)
        
        self.title = QLabel()
        self.title.setObjectName("settingsSectionContentCaption")
        self.main_layout.addWidget(self.title)

        self.icons_layout = QHBoxLayout()
        self.icons_layout.setSpacing(22)
        self.main_layout.addLayout(self.icons_layout)
        for icon in ("01d", "02d", "01n", "02n", "03n"):
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container.setFixedSize(QSize(self.ICON_LABEL_SIZE, self.ICON_LABEL_SIZE))
            container.setObjectName("settingsIconLabel")
            lbl = QLabel(parent=container)
            lbl.setPixmap(QPixmap(get_image_path(f"{folder}/{icon}.png")).scaled(
                self.ICON_SIZE, self.ICON_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            lbl.setFixedSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
            # container_layout.addWidget(lbl)
            lbl.move(-77, -77)
            self.icons_layout.addWidget(container)
    
    def click_handler(self):
        if self.objectName() == "selectedIconListCard": # Перевіряємо, чи вже обраний цей список
            return
        for icon_list_card in self.icons_list_cards:
            if icon_list_card.check_is_selected():
                icon_list_card.setObjectName("") 
                refresh_widget(icon_list_card)
        self.setObjectName("selectedIconListCard")
        refresh_widget(self)
        self.click_callback() # Активуємо кнопку збереження

    def check_is_selected(self):
        return True if self.objectName() == "selectedIconListCard" else False