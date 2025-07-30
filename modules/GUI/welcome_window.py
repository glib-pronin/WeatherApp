from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon
from ..read_qss import read_qss_file
from ..get_static import get_image_path
from ..get_weather_data import get_weather
from .click_filter import ClickFilter
from .main_window import MainAppWindow
import os

app = QApplication([])
app.setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file("dark.qss"))

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.setWindowTitle("WeatherApp")
        self.setFixedSize(QSize(width, height))
        self.click_filter = ClickFilter(self.open_main_window)
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
        self.refresh_btn.setFixedSize(QSize(50, 50))
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(lambda: self.get_data(city_name="Дніпро"))

        self.city_lbl = QLabel(text="Дніпро")
        self.city_lbl.setObjectName("city")

        self.weather_img = QLabel()
        self.weather_img.setPixmap(QPixmap(get_image_path("icons/02d.png")).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.temp_value = QLabel(text="28°")
        self.temp_value.setObjectName("tempValue")

        self.desc_lbl = QLabel(text="Хмарно")
        self.desc_lbl.setObjectName("description")
        self.range_lbl = QLabel(text="Макс.:11°, мін.:0°")
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
        # self.get_data(city_name="Дніпро")

    def get_data(self, city_name="Дніпро"):
        data = get_weather(city_name)
        print(data)
        if not data:
            print("Помилка отримання даних з API")     
        self.city_lbl.setText(city_name)
        self.temp_value.setText(f"{round(data['main']['temp'])}°")
        icon = self.check_icon(data['weather'][0]['icon'])
        self.weather_img.setPixmap(QPixmap(get_image_path(f"icons/{icon}.png")).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.desc_lbl.setText(data["weather"][0]["description"].capitalize())
        self.range_lbl.setText(f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°")

    def check_icon(self, icon: str):
        if f"{icon}.png" in os.listdir(get_image_path("icons")):
            return icon
        return "02d"
    
    def open_main_window(self):
        self.main_window = MainAppWindow(1200, 600)
        self.main_window.show()
        self.close()


    
main_window = MainWindow(350, 350)
main_window.show()

