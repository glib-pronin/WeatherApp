from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from .app_size import AppSizeWidget
from .app_language import AppLangWidget
from .icons_list import IconsListWidget
from .city_search import CitySearchWidget
from ..click_filter import ClickFilter
from ...Tools import refresh_widget, get_json

class SettingsModal(QDialog):
    MODAL_HEIGHT = 688
    MODAL_WIDTH = 790
    MAIN_CONTENT_HEIGHT = 578
    mainContentDataChangedSignal = pyqtSignal(object)
 
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.lang = get_json("config.json")["selected_lang"]
        self.lang_dict = get_json("translations.json")
        self.old_pos = None
        # Основний контейнер
        self.container_layout = QVBoxLayout(self)
        self.container = QWidget()
        self.container.setFixedSize(QSize(self.MODAL_WIDTH, self.MODAL_HEIGHT))
        self.container.setObjectName("settingsModal")
        self.container_layout.addWidget(self.container)
        self.click_filter = ClickFilter(self.close)
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(34)
        # Надпис "Налаштування" та кнопка закриття
        self.first_line = QHBoxLayout()
        self.text_lbl = QLabel(text=self.lang_dict[self.lang]["settings_caption"])
        self.text_lbl.setObjectName("settingsTitle")
        self.first_line.addWidget(self.text_lbl)
        self.close_btn = QLabel(text="✕")
        self.close_btn.installEventFilter(self.click_filter)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setObjectName("settingsTitle")
        self.first_line.addStretch()
        self.first_line.addWidget(self.close_btn)
        self.main_layout.addLayout(self.first_line)
        # Основні layouts
        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setSpacing(16)
        self.side_panel_layout = QVBoxLayout()
        self.side_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_panel_layout.setSpacing(0)
        self.main_content_layout.addLayout(self.side_panel_layout)
        self.main_layout.addLayout(self.main_content_layout)
        # Надписи секцій налаштувань, масив для керування обраної
        self.sections_lbl = []
        self.city_search_lbl = SectionLabel("searching_city_section", self.side_panel_layout, self.sections_lbl, CitySearchWidget, self.change_main_content_widget)
        self.app_size_lbl = SectionLabel("app_size_section", self.side_panel_layout, self.sections_lbl, AppSizeWidget, self.change_main_content_widget)
        self.app_language_lbl = SectionLabel("app_lang_section", self.side_panel_layout, self.sections_lbl, AppLangWidget, self.change_main_content_widget)
        self.icons_list_lbl = SectionLabel("icons_list_section", self.side_panel_layout, self.sections_lbl, IconsListWidget, self.change_main_content_widget)
        self.sections_lbl.extend([self.city_search_lbl, self.app_size_lbl, self.app_language_lbl, self.icons_list_lbl])
        for lbl in (self.city_search_lbl, self.app_size_lbl, self.app_language_lbl, self.icons_list_lbl):
            lbl.set_label_text(self.lang_dict, self.lang)
        # Основний контент
        self.main_content = QWidget()
        self.main_content_layout.addWidget(self.main_content)
        self.city_search_lbl.click_handler()

    def change_main_content_widget(self, widget_cls):
        new_main_content = widget_cls(self.MAIN_CONTENT_HEIGHT, self.lang, self.lang_dict) # Зміна основного контенту
        self.main_content_layout.removeWidget(self.main_content)
        self.main_content.deleteLater() # Видаляємо старий віджет
        self.main_content_layout.addWidget(new_main_content)
        self.main_content = new_main_content
        self.main_content.dataChangedSignal.connect(self.handle_data_signal) # Новий сигнал 

    def handle_data_signal(self, data):
        if list(data.keys())[0] == "selected_lang": # Якщо зміна мови, то спочатку оновимо налаштування, потім передаємо сигнал
            self.update_lang(data["selected_lang"])
            self.main_content.change_lang(self.lang)
        self.mainContentDataChangedSignal.emit(data)

    def update_lang(self, lang):
        self.lang = lang
        self.text_lbl.setText(self.lang_dict[self.lang]["settings_caption"])
        for lbl in self.sections_lbl:
            lbl.set_label_text(self.lang_dict, self.lang)

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.old_pos = a0.globalPosition().toPoint()
        return super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0):
        if self.old_pos:
            delta = a0.globalPosition().toPoint() - self.old_pos
            self.move(self.pos()+delta)
            self.old_pos = a0.globalPosition().toPoint()
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0):
        self.old_pos = None
        return super().mouseReleaseEvent(a0)


class SectionLabel(QLabel):
    LABEL_WIDTH = 158
    LABEL_HEIGHT = 35

    def __init__(self, key_for_text, parent: QVBoxLayout, lbl_list, widget_cls, change_callback):
        super().__init__()
        parent.addWidget(self)
        self.setContentsMargins(8, 0, 0, 0)
        self.setFixedSize(QSize(self.LABEL_WIDTH, self.LABEL_HEIGHT))
        self.setObjectName("sectionLabel")
        self.key_for_text = key_for_text
        self.click_filter = ClickFilter(self.click_handler)
        self.installEventFilter(self.click_filter)
        self.lbl_list = lbl_list
        self.widget_cls = widget_cls
        self.change_callback = change_callback

    def set_label_text(self, lang_dict, lang):
        self.setText(lang_dict[lang][self.key_for_text])

    def click_handler(self):
        if self.objectName() == "selectedSectionLabel":
            return
        for lbl in self.lbl_list:
            if lbl.objectName() == "selectedSectionLabel":
                lbl.setObjectName("sectionLabel")
                refresh_widget(lbl)
        self.setObjectName("selectedSectionLabel")
        self.change_callback(self.widget_cls)
        refresh_widget(self)
