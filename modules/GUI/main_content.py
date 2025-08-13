from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from ..Tools import get_image_path
from .click_filter import ClickFilter
from .MainContent import WeatherWidget, TimeWidget, ForecastWidget

class MainContent(QWidget):

    SEARCHING_PANEL_HEIGHT = 36
    BASE_ADDING_WIDTH = 100
    ERROR_PADDING = 45
    INPUT_WIDTH = 225
    ICON_SIZE = 12

    def __init__(self, width, height, config_data, on_click_callback):
        print(width, height)
        super().__init__()
        # self.setFixedSize(QSize(width, height))
        self.setObjectName("mainContent")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.click_filter = ClickFilter(on_click_callback)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(10, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.top_panel = QHBoxLayout()

        self.adding_frame = QWidget()
        self.adding_frame.setFixedSize(QSize(self.BASE_ADDING_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.adding_frame.setObjectName("cityAddFrame")
        self.adding_layout = QHBoxLayout(self.adding_frame)
        self.plus_icon = QLabel(text="+")
        self.plus_icon.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.plus_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plus_icon.setObjectName("plusIcon")
        self.frame_text = QLabel(text="Додати")
        self.frame_text.setObjectName("cityAddFrameText")
        self.adding_layout.addWidget(self.plus_icon)
        self.adding_layout.addWidget(self.frame_text)
        self.adding_frame.setVisible(False)
        self.adding_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.adding_frame.installEventFilter(self.click_filter)

        self.search_layout = QHBoxLayout()
        self.search_icon = QLabel()
        self.search_icon.setFixedSize(QSize(self.SEARCHING_PANEL_HEIGHT, self.SEARCHING_PANEL_HEIGHT))
        self.search_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_icon.setObjectName("searchIcon")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setFixedSize(QSize(self.INPUT_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.search_input.textEdited.connect(self.show_adding_frame)

        self.search_layout.addWidget(self.search_icon)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.setSpacing(0)
        self.top_panel.addWidget(self.adding_frame)
        self.top_panel.addLayout(self.search_layout)
        self.top_panel.setSpacing(10)
        self.top_panel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addLayout(self.top_panel)
        
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
        self.main_layout.addLayout(self.panels_layout)
        self.set_icons(config_data["selected_theme"])

    def resizeEvent(self, a0):
        self.city_info_layout.setSpacing(self.width()//79)
        return super().resizeEvent(a0)

    def set_icons(self, theme: str):
        self.search_icon.setPixmap(QPixmap(get_image_path(f"images/search_icon_{theme}.png")).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        if isinstance(self.forecast_info_widget, ForecastWidget):
            self.forecast_info_widget.update_btn_icons(theme)
    
    def show_adding_frame(self):
        self.adding_frame.setVisible(bool(self.search_input.text().strip()))
        self.normalize_adding_frame()

    def handle_search_result(self, success: bool, error: str = None):
        self.search_input.clear()
        if success:
            self.adding_frame.setVisible(False)
            return
        self.normalize_adding_frame(text=error, plus_visible=False)

    def normalize_adding_frame(self, text: str = "Додати", plus_visible: bool = True):
        self.frame_text.setText(text)
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
        self.refresh_style(self.adding_frame)
        self.refresh_style(self.frame_text)
        self.adding_frame.setFixedWidth(frame_width)

    def update_main_content(self, city_frame):
        self.new_weather_info_widget = WeatherWidget(height=303, city_frame=city_frame)
        self.weather_info_widget = self.replace_widget(self.weather_info_widget, self.new_weather_info_widget, self.city_info_layout)
        self.new_time_info_widget = TimeWidget(height=303, city_date_time=city_frame.date_time)
        self.time_info_widget = self.replace_widget(self.time_info_widget, self.new_time_info_widget, self.city_info_layout)
        self.new_forecast_info_widget = ForecastWidget(height=157, city_name=city_frame.city_name.text(), city_desc=city_frame.weather_desc.text())
        self.forecast_info_widget = self.replace_widget(self.forecast_info_widget, self.new_forecast_info_widget, self.panels_layout)

    def replace_widget(self, old_widget, new_widget, layout):
        layout.removeWidget(old_widget)
        old_widget.deleteLater()
        layout.addWidget(new_widget)
        return new_widget


    def refresh_style(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)

