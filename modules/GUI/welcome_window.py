from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon
from ..Tools import *
from .click_filter import ClickFilter
from .main_window import MainAppWindow
import os

app = QApplication([])
app.setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file(f"{get_json('config.json')['selected_theme']}.qss"))

class MainWindow(QMainWindow):
    def __init__(self, width, height, window_name):
        super().__init__()
        self.window_name = window_name
        self.setWindowTitle(window_name)
        self.setFixedSize(QSize(width, height))
        self.click_filter = ClickFilter(self.open_main_window)
        self.config_data = get_json("config.json")

        self.weather_widget = QWidget()
        self.weather_widget.installEventFilter(self.click_filter)
        self.weather_widget.setObjectName("weatherWidget")

        self.weather_widget_layout = QVBoxLayout(self.weather_widget)
        self.weather_widget_layout.setSpacing(20)
        self.weather_widget_layout.setContentsMargins(20, 20, 20, 20)
        self.weather_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.position_layout = QHBoxLayout()
        self.position_layout.setSpacing(10)
        self.position_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp_layout = QHBoxLayout()
        self.temp_layout.setSpacing(10)
        self.temp_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.small_layout = QVBoxLayout()
        self.small_layout.setSpacing(5)


        self.position_img = QLabel()
        self.position_img.setPixmap(QPixmap(get_image_path("images/vector.png")).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.position_lbl = QLabel(text="Поточна позиція")
        self.position_lbl.setObjectName("position")
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon(get_image_path("images/refresh.png")))
        self.refresh_btn.setIconSize(QSize(44, 44))
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(lambda: self.get_data(city_name=self.config_data["selected_city_name"]))

        self.city_lbl = QLabel(text="-")
        self.city_lbl.setObjectName("city")

        self.weather_img = QLabel()
        self.temp_value = QLabel(text="-°")
        self.temp_value.setObjectName("tempValue")

        self.desc_lbl = QLabel(text="")
        self.desc_lbl.setObjectName("description")
        self.range_lbl = QLabel(text="—")
        self.range_lbl.setObjectName("tempRange")

        self.position_layout.addWidget(self.position_img)
        self.position_layout.addWidget(self.position_lbl)
        self.position_layout.addStretch()
        self.position_layout.addWidget(self.refresh_btn)
        self.weather_widget_layout.addLayout(self.position_layout)
        self.weather_widget_layout.addWidget(self.city_lbl)
        self.temp_layout.addWidget(self.weather_img)
        self.temp_layout.addWidget(self.temp_value)
        self.weather_widget_layout.addLayout(self.temp_layout)
        self.small_layout.addWidget(self.desc_lbl)
        self.small_layout.addWidget(self.range_lbl)
        self.weather_widget_layout.addLayout(self.small_layout)

        self.setCentralWidget(self.weather_widget)
        self.get_data(city_name=self.config_data["selected_city_name"])

    def get_data(self, city_name):
        data = get_weather(city_name)
        # data = None
        print(data)
        if not data:
            print("Помилка отримання даних з API")   
            self.desc_lbl.setText("Помилка отримання даних")
            return  
        self.city_lbl.setText(city_name)
        self.temp_value.setText(f"{round(data['main']['temp'])}°")
        icon = self.check_icon(data['weather'][0]['icon'])
        weather_type = select_weather_type(icon)
        self.weather_widget.setObjectName(weather_type)
        self.refresh_style(self.weather_widget)
        self.weather_img.setPixmap(QPixmap(get_image_path(f"icons/{icon}.png")).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.desc_lbl.setText(data["weather"][0]["description"].capitalize())
        self.range_lbl.setText(f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°")

    def check_icon(self, icon: str):
        if f"{icon}.png" in os.listdir(get_image_path("icons")):
            return icon
        return "02d"
    
    def refresh_style(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)
    
    def open_main_window(self):
        self.main_window = MainAppWindow(1200, 600, self.window_name, self.config_data)
        self.main_window.show()
        self.close()


    
main_window = MainWindow(350, 350, "WeatherApp")
main_window.show()

