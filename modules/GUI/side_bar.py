from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QApplication
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon
from ..read_qss import read_qss_file
from ..get_static import get_image_path
from ..get_json_data import get_json
from ..get_weather_data import get_weather
from ..get_time import get_local_time
from .city_frame import CityFrame

class SideBar(QWidget):
    def __init__(self, width, height, switch_theme_callback, refresh_style):
        super().__init__()
        self.setFixedSize(width, height)
        self.setObjectName("sideBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.switch_theme_callback = switch_theme_callback
        self.refresh_style = refresh_style
        self.cities_names = None
        self.cities_list = []

        self.side_bar_layout = QVBoxLayout(self)
        self.side_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_bar_layout.setContentsMargins(10, 20, 20, 10)
        self.side_bar_layout.setSpacing(10)

        self.theme_switcher = QPushButton()
        self.theme_switcher.setObjectName("themeSwitcher")
        self.theme_switcher.setFixedSize(QSize(52, 24))
        self.set_theme_icon("dark")
        self.theme_switcher.clicked.connect(self.switch_theme_callback)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(360)
        self.scroll_area.setObjectName("scrollArea")

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(5)

        self.side_bar_layout.addWidget(self.theme_switcher, alignment=Qt.AlignmentFlag.AlignRight)
        self.side_bar_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)

        self.init_cities()
        self.selected_city = self.cities_list[0] if self.cities_list else None

    def trigger_click(self):
        if self.selected_city:
            self.selected_city.trigger_click()

    def add_city_frame(self, name, code, time, temp, desc, tmax, tmin):
        city = CityFrame(name, code, time, temp, desc, tmax, tmin, self.switch_theme_callback)
        self.scroll_layout.addWidget(city)
        self.cities_list.append(city)
        QTimer.singleShot(0, lambda c=name, f=city: self.load_weather(c, f))
    
    def init_cities(self):
        self.cities_names = get_json("cities.json")["cities"]
        for city in self.cities_names:
            self.add_city_frame(
                city, code=None, 
                time="Завантаження...", temp=None, desc="Завантаження...", 
                tmax=None, tmin=None
                )     
            
    def load_weather(self, city_name, frame):
        data = get_weather(city_name)
        if data:  
            local_time = get_local_time(timezone=data["timezone"])
            frame.update_weather(
                code=data['weather'][0]['icon'], 
                time=local_time, temp=data['main']['temp'], desc=data["weather"][0]["description"], 
                tmax=data['main']['temp_max'], tmin=data['main']['temp_min']
                )
        if self.selected_city == frame:
            self.trigger_click()
                
    def apply_theme(self, city_frame=None, change_theme=True, theme=None):
        if city_frame:
            self.choose_city_frame(city_frame)
        self.set_theme_icon(theme)

    def choose_city_frame(self, city_frame):
        if self.selected_city:
            self.selected_city.setObjectName("cityFrame")
            self.refresh_style(self.selected_city)
        self.selected_city = city_frame
        self.selected_city.setObjectName("selectedCity")
        self.refresh_style(self.selected_city)

    def set_theme_icon(self, theme):
        self.theme_switcher.setIcon(QIcon(get_image_path(f"images/{theme}.png")))
        self.theme_switcher.setIconSize(QSize(20, 20))
