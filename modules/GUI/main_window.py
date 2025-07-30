from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from ..read_qss import read_qss_file
from ..get_json_data import get_json
from .side_bar import SideBar

class MainAppWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)

        self.theme = "dark"
        self.weather_types = get_json("weather_types.json")

        self.central_widget = QWidget()
        self.central_widget.setObjectName("weatherWidget")
        self.central_widget_layout = QHBoxLayout(self.central_widget)
        self.central_widget_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.side_bar = SideBar(380, height, self.switch_theme, self.refresh_style)
        self.central_widget_layout.addWidget(self.side_bar)

        self.setCentralWidget(self.central_widget)

        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(60000)

    def switch_theme(self, city_frame=None, change_theme=True):
        if change_theme:
            self.theme = "light" if self.theme == "dark" else "dark"
            QApplication.instance().setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file(f"{self.theme}.qss"))
        if city_frame:
            print(city_frame.img_code)
            weather_type = self.select_weather_type(city_frame.img_code)
            self.central_widget.setObjectName(weather_type)
            self.refresh_style(self.central_widget)
        self.side_bar.apply_theme(city_frame, change_theme, self.theme)

    def select_weather_type(self, img_code):
        for type, codes in self.weather_types.items():
            if img_code in codes:
                return type
        return "weatherWidget"

    def refresh_style(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)

    def update_weather(self):
        if self.side_bar.cities_list:
            for city in self.side_bar.cities_list:
                print(f"update {city.city_name.text()}")
                self.side_bar.load_weather(city_name=city.city_name.text(), frame=city)