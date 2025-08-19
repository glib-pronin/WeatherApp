from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from ..Tools import *
from .side_bar import SideBar
from .main_content import MainContent

class MainAppWindow(QMainWindow):
    SIDEBAR_WIDTH = 380
    UPDATE_INTERVAL = 60000

    def __init__(self, width, height, window_name, config_data):
        super().__init__()
        self.setMinimumSize(width, height)
        self.setWindowTitle(window_name)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.theme = config_data["selected_theme"]
        # Основний віджет
        self.central_widget = QWidget()
        self.central_widget.setObjectName("weatherWidget")
        self.central_widget_layout = QHBoxLayout(self.central_widget)
        self.central_widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)
        # Бокова панель та основний контент
        self.side_bar = SideBar(self.SIDEBAR_WIDTH, self.switch_theme, self.refresh_style, config_data)
        self.main_content = MainContent(width-380, height, config_data, self.add_new_city)
        self.central_widget_layout.addWidget(self.side_bar)
        self.central_widget_layout.addWidget(self.main_content)
        self.setCentralWidget(self.central_widget)
        # Таймер, який оновлює дані кожну хвилину
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(self.UPDATE_INTERVAL)

    def switch_theme(self, city_frame=None, change_theme=True):
        if change_theme: # Якщо зміна теми
            self.theme = "light" if self.theme == "dark" else "dark"
            change_file("config.json", key="selected_theme", value=self.theme)
            self.main_content.set_icons(self.theme)
            QApplication.instance().setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file(f"{self.theme}.qss"))
        if city_frame: # Якщо обране місто
            print(city_frame.img_code)
            weather_type = select_weather_type(city_frame.img_code)
            change_file("config.json", key="selected_city_name", value=city_frame.city_name.text())
            self.central_widget.setObjectName(weather_type)
            self.refresh_style(self.central_widget)
            self.main_content.update_main_content(city_frame)
        self.side_bar.apply_theme(city_frame, self.theme)

    def refresh_style(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)

    def update_weather(self):
        for city in self.side_bar.cities_list:
            print(f"update {city.city_name.text()}")
            self.side_bar.load_weather(city_name=city.city_name.text(), frame=city)

    def add_new_city(self):
        city_name = self.main_content.search_input.text().strip().capitalize()
        if city_name in self.side_bar.cities_names: # Чи вже наявне таке місто
            self.main_content.handle_search_result(False, error = "Місто вже додане")
            return
        data = get_weather(city_name, forecast_type="current")
        if not data: # Чи отримали дані
            self.main_content.handle_search_result(False, error="Місто не знайдено")
            return
        self.main_content.handle_search_result(True)
        code = data['weather'][0]['icon']
        validated_code = code if code != "50n" and code != "50d" else "04n"
        self.side_bar.add_city_frame(
            name=city_name, code=validated_code, 
            date_time=get_local_date_time(timezone=data["timezone"]), 
            temp=data['main']['temp'], desc=data["weather"][0]["description"], 
            tmax=data['main']['temp_max'], tmin=data['main']['temp_min'], eng_name=data["name"], have_data=True
        )
        self.side_bar.cities_names.append(city_name)
        change_file("config.json", key="cities", value=self.side_bar.cities_names)