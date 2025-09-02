from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QApplication
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon
from ..Tools import *
from .city_frame import CityFrame

class SideBar(QWidget):
    SWITCHER_HEIGHT = 24
    SWITCHER_WIDTH = 52
    SCROLL_WIDTH = 360

    def __init__(self, width, switch_theme_callback, config_data, lang_dict):
        super().__init__()
        self.setFixedWidth(width)
        self.setObjectName("sideBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.switch_theme_callback = switch_theme_callback
        self.cities_names = config_data["cities"]
        self.cities_list = []
        self.lang = config_data["selected_lang"]
        self.lang_dict = lang_dict
        # Головний layout
        self.side_bar_layout = QVBoxLayout(self)
        self.side_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_bar_layout.setContentsMargins(10, 20, 20, 10)
        # Перемикач теми
        self.theme_switcher = QPushButton()
        self.theme_switcher.setObjectName("themeSwitcher")
        self.theme_switcher.setFixedSize(QSize(self.SWITCHER_WIDTH, self.SWITCHER_HEIGHT))
        self.set_theme_icon(config_data["selected_theme"])
        self.theme_switcher.clicked.connect(self.switch_theme_callback)
        # Панель з містами
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
        # Завантаження збережених міст та показ обраного
        self.init_cities()
        self.selected_city = self.set_selected_city(config_data)
                
    def set_selected_city(self, config_data):
        for city in self.cities_list:
            if city.name == config_data["selected_city_name"]:
                return city

    def add_city_frame(self, name, code, date_time, temp, desc, tmax, tmin, eng_name, have_data=None):
        city = CityFrame(name, code, date_time, temp, desc, tmax, tmin, eng_name, self.switch_theme_callback)
        city.change_city_name(name if self.lang == "ua" else eng_name)
        self.scroll_layout.addWidget(city)
        self.cities_list.append(city)
        if have_data: # Якщо всі дані вже є, то QTimer не потрібен 
            city.trigger_click()
            return
        QTimer.singleShot(0, lambda c=name, f=city: self.load_weather(c, f, self.lang))
    
    def init_cities(self):
        for city, city_eng in zip(self.cities_names["ua"], self.cities_names["eng"]):
            self.add_city_frame( # Завантажуємо міста із заглушками
                city, code=None, 
                date_time=self.lang_dict[self.lang]["downloading_message"], 
                temp=None, desc=self.lang_dict[self.lang]["downloading_message"], 
                tmax=None, tmin=None, eng_name=city_eng
                )     
            
    def load_weather(self, city_name, frame, lang):
        data = get_weather(frame.eng_name, forecast_type="current", lang=lang)
        if data:  
            local_date_time = get_local_date_time(timezone=data["timezone"])
            code = data['weather'][0]['icon'] 
            frame.update_weather(
                code=code, 
                date_time=local_date_time, temp=data['main']['temp'], desc=data["weather"][0]["description"], 
                tmax=f"{self.lang_dict[self.lang]['max_text']}{round(data['main']['temp_max'])}", 
                tmin=f"{self.lang_dict[self.lang]['min_text']}{round(data['main']['temp_min'])}"
                )
        else:
            frame.update_weather(
                code=None, 
                date_time=self.lang_dict[self.lang]["downloading_message"], 
                temp=None, desc=self.lang_dict[self.lang]["downloading_message"], 
                tmax=None, tmin=None
                )   
        frame.change_city_name(city_name if lang == "ua" else frame.eng_name)
        if self.selected_city == frame:
            self.selected_city.trigger_click()
                
    def apply_theme(self, city_frame=None, theme=None):
        if city_frame:
            self.choose_city_frame(city_frame)
        else:
            self.set_theme_icon(theme)

    def choose_city_frame(self, city_frame):
        if self.selected_city:
            self.selected_city.setObjectName("cityFrame")
            refresh_widget(self.selected_city)
        self.selected_city = city_frame
        self.selected_city.setObjectName("selectedCity")
        refresh_widget(self.selected_city)

    def set_theme_icon(self, theme):
        self.theme_switcher.setIcon(QIcon(get_image_path(f"images/{theme}.png")))
        self.theme_switcher.setIconSize(QSize(20, 20))

    def delete_city(self, index):
        print(index)
        self.scroll_layout.removeWidget(self.cities_list[index])
        self.cities_list[index].deleteLater()
        self.cities_list.pop(index)
        if self.check_selected_city(index):
            self.selected_city = None
            change_file("config.json", "selected_city_name", "")
        self.cities_names["ua"].pop(index)
        self.cities_names["eng"].pop(index)
        change_file("config.json", "cities", self.cities_names)
        
    def check_selected_city(self, index):
        if self.selected_city:
            return self.cities_names[self.lang][index] == self.selected_city.city_name.text()