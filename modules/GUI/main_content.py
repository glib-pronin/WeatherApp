from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCompleter
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QStringListModel
from PyQt6.QtGui import QPixmap
from ..Tools import get_image_path, refresh_widget, get_json
from .click_filter import ClickFilter
from .Settings import SettingsModal
from .MainContent import WeatherWidget, TimeWidget, ForecastWidget, HourlyWidget

class MainContent(QWidget):
    SEARCHING_PANEL_HEIGHT = 36
    BASE_ADDING_WIDTH = 100
    ERROR_PADDING = 45
    INPUT_WIDTH = 225
    ICON_SIZE = 12
    FORECAST_WIDGET_HEIGHT = 157
    HOURLY_WIDGET_HEIGHT = 205
    SETTINGS_BLOCK = 36
    propagatedSignal = pyqtSignal(object)

    def __init__(self, width, height, config_data, on_click_callback, lang_dict):
        print(width, height)
        super().__init__()
        self.setObjectName("mainContent")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.click_filter = ClickFilter(on_click_callback)
        self.click_filter_settings = ClickFilter(self.open_modal)
        self.current_city = None
        self.lang = config_data["selected_lang"]
        self.lang_dict = lang_dict
        # Основний layout 
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 20, 10)
        self.main_layout.setSpacing(20)
        self.top_panel = QHBoxLayout()  # верхня панель для пошуку та додавання
        # Налаштування
        self.settings_layout = QHBoxLayout()
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settings_widget = QLabel()
        self.settings_widget.setFixedSize(QSize(self.SETTINGS_BLOCK, self.SETTINGS_BLOCK))
        self.settings_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.settings_widget.setObjectName("settingsBlock")
        self.settings_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_layout.addWidget(self.settings_widget)
        self.settings_widget.installEventFilter(self.click_filter_settings)
        self.settings_text = QLabel(text=self.lang_dict[self.lang]["settings_caption"])
        self.settings_text.setObjectName("settingsText")
        self.settings_layout.addWidget(self.settings_text)
        self.top_panel.addLayout(self.settings_layout)
        # Кнопка додавання 
        self.adding_frame = QWidget()
        self.adding_frame.setFixedSize(QSize(self.BASE_ADDING_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.adding_frame.setObjectName("cityAddFrame")
        self.adding_layout = QHBoxLayout(self.adding_frame)
        self.plus_icon = QLabel(text="+")
        self.plus_icon.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.plus_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plus_icon.setObjectName("plusIcon")
        self.frame_text = QLabel(text=self.lang_dict[self.lang]["adding_caption"])
        self.frame_text_key = "adding_caption"
        self.frame_text.setObjectName("cityAddFrameText")
        self.adding_layout.addWidget(self.plus_icon)
        self.adding_layout.addWidget(self.frame_text)
        self.adding_frame.setVisible(False)
        self.adding_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.adding_frame.installEventFilter(self.click_filter)
        # Поле пошуку
        self.search_layout = QHBoxLayout()
        self.search_icon = QLabel()
        self.search_icon.setFixedSize(QSize(self.SEARCHING_PANEL_HEIGHT, self.SEARCHING_PANEL_HEIGHT))
        self.search_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_icon.setObjectName("searchIcon")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setFixedSize(QSize(self.INPUT_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.search_input.setPlaceholderText(self.lang_dict[self.lang]["place_holder"])
        self.search_input.textEdited.connect(self.show_adding_frame)
        self.search_layout.addWidget(self.search_icon)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.setSpacing(0)
        self.top_panel.addWidget(self.adding_frame)
        self.top_panel.addLayout(self.search_layout)
        self.top_panel.setSpacing(10)
        self.top_panel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addLayout(self.top_panel)
        # QCompleter
        self.grouped_cities = get_json("grouped_cities.json")
        self.prefix = ""
        self.completer = QCompleter()
        # popup = self.completer.popup()
        # popup.setObjectName("popup") 
        # .setStyleSheet("""
        #     QListView {
        #         background-color: #1e1e1e;
        #         color: #f0f0f0;
        #         border: 1px solid #555;
        #         selection-background-color: #0078d7;
        #         selection-color: white;
        #         font-size: 14px;
        #         padding: 4px;
        #     }
        #     QListView::item {
        #         padding: 15px;
        #     }
        # """)
        self.search_input.setCompleter(self.completer)
        # Основні панелі: місто, час, прогноз на 5 днів
        self.panels_layout = QVBoxLayout()
        self.panels_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.panels_layout.setSpacing(10)
        self.city_info_layout = QHBoxLayout()
        self.weather_info_widget = QWidget()
        self.city_info_layout.addWidget(self.weather_info_widget)
        self.time_info_widget = QWidget()
        self.city_info_layout.addWidget(self.time_info_widget)
        self.city_info_layout.setSpacing(10)
        self.panels_layout.addLayout(self.city_info_layout)
        self.forecast_info_widget = QWidget()
        self.panels_layout.addWidget(self.forecast_info_widget)
        self.hourly_info_widget = QWidget()
        self.panels_layout.addWidget(self.hourly_info_widget)
        self.main_layout.addLayout(self.panels_layout)
        self.set_icons(config_data["selected_theme"]) # Встановлюємо потрібні іконки

    def open_modal(self):
        self.settings_modal = SettingsModal()
        self.settings_modal.show()
        self.settings_modal.mainContentDataChangedSignal.connect(self.propagatedSignal.emit) # Перенаправляємо сигнал на головне вікно для основних дій

    def resizeEvent(self, a0):
        self.city_info_layout.setSpacing(self.width()//79)
        return super().resizeEvent(a0)

    def set_icons(self, theme: str):
        self.settings_widget.setPixmap(QPixmap(get_image_path(f"images/settings_{theme}.png")).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.search_icon.setPixmap(QPixmap(get_image_path(f"images/search_icon_{theme}.png")).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        if isinstance(self.forecast_info_widget, ForecastWidget):
            self.forecast_info_widget.update_btn_icons(theme)
        if isinstance(self.hourly_info_widget, HourlyWidget):
            self.hourly_info_widget.update_weather_icons(theme)
    
    def show_adding_frame(self):
        input_text = self.search_input.text().strip()
        self.adding_frame.setVisible(bool(input_text))
        self.normalize_adding_frame()
        if len(input_text) >= 3 and input_text[:3] != self.prefix: # Якщо юзер ввів мінімум 3 символи і вони нові
            self.prefix = input_text[:3] # Отримуємо префікс
            city_list = self.grouped_cities[self.lang].get(input_text[:3]) 
            self.completer.setModel(QStringListModel(city_list)) # Завантажуємо нові міста для completer
        
    def handle_search_result(self, success: bool, error_key: str = None):
        self.search_input.clear()
        if success:
            self.adding_frame.setVisible(False)
            return
        self.normalize_adding_frame(text_key=error_key, plus_visible=False)

    def normalize_adding_frame(self, text_key: str = "adding_caption", plus_visible: bool = True):
        self.frame_text.setText(self.lang_dict[self.lang][text_key])
        self.frame_text_key = text_key
        self.plus_icon.setVisible(plus_visible)
        if plus_visible:
            frame_width = self.BASE_ADDING_WIDTH
            self.frame_text.setObjectName("cityAddFrameText")
            self.adding_frame.setObjectName("cityAddFrame")
            self.adding_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            frame_width = self.frame_text.sizeHint().width()+self.ERROR_PADDING
            self.adding_frame.setObjectName("searchingError")
            self.frame_text.setObjectName("searchingError")
            self.adding_frame.setCursor(Qt.CursorShape.ArrowCursor)
        refresh_widget(self.adding_frame)
        refresh_widget(self.frame_text)
        self.adding_frame.setFixedWidth(frame_width)

    def update_main_content(self, city_frame):
        new_weather_info_widget = WeatherWidget(height=303, city_frame=city_frame)
        self.weather_info_widget = self.replace_widget(self.weather_info_widget, new_weather_info_widget, self.city_info_layout)
        new_time_info_widget = TimeWidget(height=303, city_date_time=city_frame.date_time, today_caption=self.lang_dict[self.lang]["today_caption"], lang=self.lang)
        self.time_info_widget = self.replace_widget(self.time_info_widget, new_time_info_widget, self.city_info_layout)
        if self.current_city != city_frame.name:
            new_forecast_info_widget = ForecastWidget(height=self.FORECAST_WIDGET_HEIGHT, city_frame=city_frame)
            self.forecast_info_widget = self.replace_widget(self.forecast_info_widget, new_forecast_info_widget, self.panels_layout)
            new_hourly_info_widget = HourlyWidget(height=self.HOURLY_WIDGET_HEIGHT, city_eng_name = city_frame.eng_name, hourly_info_caption=self.lang_dict[self.lang]["hourly_info_caption"])
            self.hourly_info_widget = self.replace_widget(self.hourly_info_widget, new_hourly_info_widget, self.panels_layout)
        self.current_city = city_frame.name

    def clear_main_content(self):
        new_weather_info_widget = QWidget()
        self.weather_info_widget = self.replace_widget(self.weather_info_widget, new_weather_info_widget, self.city_info_layout)
        new_time_info_widget = QWidget()
        self.time_info_widget = self.replace_widget(self.time_info_widget, new_time_info_widget, self.city_info_layout)
        new_forecast_info_widget = QWidget()
        self.forecast_info_widget = self.replace_widget(self.forecast_info_widget, new_forecast_info_widget, self.panels_layout)
        new_hourly_info_widget = QWidget()
        self.hourly_info_widget = self.replace_widget(self.hourly_info_widget, new_hourly_info_widget, self.panels_layout)
        self.current_city = None

    def replace_widget(self, old_widget, new_widget, layout):
        layout.removeWidget(old_widget)
        old_widget.deleteLater()
        layout.addWidget(new_widget)
        return new_widget
    
    def update_lang(self, lang):
        self.lang = lang
        self.settings_text.setText(self.lang_dict[self.lang]["settings_caption"])
        self.frame_text.setText(self.lang_dict[self.lang][self.frame_text_key])
        self.search_input.setPlaceholderText(self.lang_dict[self.lang]["place_holder"])
        if hasattr(self.time_info_widget, "update_lang"):
            self.forecast_info_widget.update_desc_lbl()
            self.time_info_widget.update_lang(self.lang_dict[self.lang]["today_caption"], self.lang)
            self.hourly_info_widget.title_label.setText(self.lang_dict[self.lang]["hourly_info_caption"])


