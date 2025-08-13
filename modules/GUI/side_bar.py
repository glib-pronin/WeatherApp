from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QApplication
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon
from ..Tools import *
from .city_frame import CityFrame

class SideBar(QWidget):

    SWITCHER_HEIGHT = 24
    SWITCHER_WIDTH = 52
    SCROLL_WIDTH = 360

    def __init__(self, width, height, switch_theme_callback, refresh_style, config_data):
        super().__init__()
        self.setFixedWidth(width)
        self.setObjectName("sideBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.switch_theme_callback = switch_theme_callback
        self.refresh_style = refresh_style
        self.cities_names = config_data["cities"]
        self.cities_list = []

        self.side_bar_layout = QVBoxLayout(self)
        self.side_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_bar_layout.setContentsMargins(10, 20, 20, 10)

        self.theme_switcher = QPushButton()
        self.theme_switcher.setObjectName("themeSwitcher")
        self.theme_switcher.setFixedSize(QSize(self.SWITCHER_WIDTH, self.SWITCHER_HEIGHT))
        self.set_theme_icon(config_data["selected_theme"])
        self.theme_switcher.clicked.connect(self.switch_theme_callback)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(self.SCROLL_WIDTH)
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollContent")

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(5)

        self.side_bar_layout.addWidget(self.theme_switcher, alignment=Qt.AlignmentFlag.AlignRight)
        self.side_bar_layout.addWidget(self.scroll_area)
        self.side_bar_layout.setSpacing(5)
        self.scroll_area.setWidget(self.scroll_content)

        self.init_cities()
        self.selected_city = self.set_selected_city(config_data)
                
    def set_selected_city(self, config_data):
        for city in self.cities_list:
            if city.city_name.text() == config_data["selected_city_name"]:
                return city

    def add_city_frame(self, name, code, date_time, temp, desc, tmax, tmin, have_data=None):
        city = CityFrame(name, code, date_time, temp, desc, tmax, tmin, self.switch_theme_callback)
        self.scroll_layout.addWidget(city)
        self.cities_list.append(city)
        if have_data:
            city.trigger_click()
            return
        QTimer.singleShot(0, lambda c=name, f=city: self.load_weather(c, f))
    
    def init_cities(self):
        for city in self.cities_names:
            self.add_city_frame(
                city, code=None, 
                date_time="Завантаження...", temp=None, desc="Завантаження...", 
                tmax=None, tmin=None
                )     
            
    def load_weather(self, city_name, frame):
        data = get_weather(city_name)
        if data:  
            local_date_time = get_local_date_time(timezone=data["timezone"])
            code = data['weather'][0]['icon'] 
            validated_code = code if code != "50n" and code != "50d" else "04n"
            frame.update_weather(
                code=validated_code, 
                date_time=local_date_time, temp=data['main']['temp'], desc=data["weather"][0]["description"], 
                tmax=data['main']['temp_max'], tmin=data['main']['temp_min']
                )
        if self.selected_city == frame:
            self.selected_city.trigger_click()
                
    def apply_theme(self, city_frame=None, change_theme=True, theme=None):
        if city_frame:
            self.choose_city_frame(city_frame)
            return
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
