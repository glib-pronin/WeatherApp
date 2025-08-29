from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from ..Tools import *
from .side_bar import SideBar
from .main_content import MainContent
from .top_bar import WindowsTopBar

class MainAppWindow(QMainWindow):
    SIDEBAR_WIDTH = 380
    UPDATE_INTERVAL = 60000
    TOP_BAR_HEIGHT = 30

    def __init__(self, width, height, config_data, object_name):
        super().__init__()
        self.setFixedSize(width, height)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.theme = config_data["selected_theme"]
        self.lang = config_data["selected_lang"]
        self.lang_dict = get_json("translations.json")
        # Основний віджет
        self.central_widget = QWidget()
        self.central_widget.setObjectName(object_name if object_name != "welcomeWidget" else "weatherWidget")
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.top_bar = WindowsTopBar(self, self.TOP_BAR_HEIGHT, "WeatherApp")
        self.central_layout.addWidget(self.top_bar)
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # Бокова панель та основний контент
        self.side_bar = SideBar(self.SIDEBAR_WIDTH, self.switch_theme, config_data, self.lang_dict)
        self.main_content = MainContent(width-380, height, config_data, self.add_new_city, self.lang_dict)
        self.main_content.propagatedSignal.connect(self.apply_settings_data)
        self.main_layout.addWidget(self.side_bar)
        self.main_layout.addWidget(self.main_content)
        self.central_layout.addLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        # Таймер, який оновлює дані кожну хвилину
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(self.UPDATE_INTERVAL)

    def apply_settings_data(self, data: dict):
        key = list(data.keys())[0] # Отримуємо ключ - назва зміни
        if key == "main_window_size": # Якщо зміна розміру
            if self.isMaximized():
                self.top_bar.toggle_btn_max()
            split_size = data[key].split("x")
            self.setFixedSize(int(split_size[0]), int(split_size[1]))
        elif key == "selected_icons_folder": # Якщо зміна іконок
            if hasattr(self.main_content.weather_info_widget, "update_weather_icon"): 
                self.main_content.weather_info_widget.update_weather_icon(data[key])
        elif key == "selected_lang": # Якщо зміна мови
            self.lang = data[key]
            self.side_bar.lang = self.lang
            self.update_weather()
            self.main_content.update_lang(self.lang)
        elif key == "delete_city": # Якщо видалено місто
            if self.side_bar.check_selected_city(data[key]): # Перевірка, чи видалено обране місто
                self.main_content.clear_main_content() # Очищаємо main content
            self.side_bar.delete_city(data[key])
            return
        elif key == "added_city": # Якщо додане місто
            inner_data = data[key]
            self.side_bar.add_city_frame(
            name=inner_data["city_ua"], code=inner_data['weather'][0]['icon'], 
            date_time=get_local_date_time(timezone=inner_data["timezone"]), 
            temp=inner_data['main']['temp'], desc=inner_data["weather"][0]["description"], 
            tmax=f"{self.lang_dict[self.lang]['max_text']}{round(inner_data['main']['temp_max'])}", 
            tmin=f"{self.lang_dict[self.lang]['min_text']}{round(inner_data['main']['temp_min'])}", eng_name=inner_data["name"], have_data=True
            )
            self.update_side_bar_lists(inner_data["city_ua"], inner_data["name"])
            return
        change_file("config.json", key=key, value=data[key]) # Якщо потрібно, змінюємо конфіг

    def switch_theme(self, city_frame=None, change_theme=True):
        if change_theme: # Якщо зміна теми
            self.theme = "light" if self.theme == "dark" else "dark"
            change_file("config.json", key="selected_theme", value=self.theme)
            self.main_content.set_icons(self.theme)
            QApplication.instance().setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file(f"{self.theme}.qss"))
        if city_frame: # Якщо обране місто
            print(city_frame.img_code)
            weather_type = select_weather_type(city_frame.img_code)
            change_file("config.json", key="selected_city_name", value=city_frame.name)
            self.central_widget.setObjectName(weather_type)
            refresh_widget(self.central_widget)
            self.main_content.update_main_content(city_frame)
        self.side_bar.apply_theme(city_frame, self.theme)

    def update_weather(self):
        for city in self.side_bar.cities_list:
            print(f"update {city.name}")
            self.side_bar.load_weather(city_name=city.name, frame=city, lang=self.lang)

    def add_new_city(self):
        city_name = self.main_content.search_input.text().strip().capitalize()
        if city_name in self.side_bar.cities_names["ua"] or city_name in self.side_bar.cities_names["eng"]: # Чи вже наявне таке місто
            self.main_content.handle_search_result(False, error_key="existed_city_error")
            return
        translated_city_name = get_translated_city_name(city_name)
        data = get_weather(translated_city_name[1], forecast_type="current", lang=self.lang) if translated_city_name else None
        if not data: # Чи отримали дані
            self.main_content.handle_search_result(False, error_key="not_found_city_error")
            return
        self.main_content.handle_search_result(True)
        code = data['weather'][0]['icon']
        validated_code = code if code != "50n" and code != "50d" else "04n"
        self.side_bar.add_city_frame(
            name=translated_city_name[0], code=validated_code, 
            date_time=get_local_date_time(timezone=data["timezone"]), 
            temp=data['main']['temp'], desc=data["weather"][0]["description"], 
            tmax=f"{self.lang_dict[self.lang]['max_text']}{round(data['main']['temp_max'])}", 
            tmin=f"{self.lang_dict[self.lang]['min_text']}{round(data['main']['temp_min'])}", eng_name=translated_city_name[1], have_data=True
        )
        self.update_side_bar_lists(translated_city_name[0], translated_city_name[1])

    def update_side_bar_lists(self, city_ua, city_eng):
        self.side_bar.cities_names["ua"].append(city_ua)
        self.side_bar.cities_names["eng"].append(city_eng)
        change_file("config.json", key="cities", value=self.side_bar.cities_names)