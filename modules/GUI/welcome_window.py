from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon
from ..Tools import *
from .click_filter import ClickFilter
from .main_window import MainAppWindow

config_data = get_json("config.json")
app = QApplication([])
app.setStyleSheet(read_qss_file("main.qss") + "\n" + read_qss_file(f"{config_data['selected_theme']}.qss"))

class MainWindow(QMainWindow):
    REFRESH_ICON_SIZE = 44
    WEATHER_IMAGE_SIZE = 76
    POSITION_IMAGE_SIZE = 16
    MAIN_WINDOW_WIDTH = int(config_data["main_window_size"].split("x")[0])
    MAIN_WINDOW_HEIGHT = int(config_data["main_window_size"].split("x")[1])

    def __init__(self, width, height, config_data):
        super().__init__()
        self.setMinimumSize(QSize(width, height))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setObjectName("welcomeWidget")
        self.click_filter = ClickFilter(self.open_main_window)
        self.config_data = config_data
        # Основний контейнер
        self.weather_widget = QWidget()
        self.weather_widget.installEventFilter(self.click_filter)
        # Усі layouts
        self.weather_widget_layout = QVBoxLayout(self.weather_widget)
        self.weather_widget_layout.setSpacing(5)
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
        # Верхній рядок з іконкою позиції, надписом та кнопкою оновлення
        self.position_img = QLabel()
        self.position_img.setPixmap(QPixmap(get_image_path("images/vector.png")).scaled(self.POSITION_IMAGE_SIZE, self.POSITION_IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.position_lbl = QLabel(text=get_json("translations.json")[self.config_data["selected_lang"]]["welcome_widget_caption"])
        self.position_lbl.setObjectName("position")
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon(get_image_path("images/refresh.png")))
        self.refresh_btn.setIconSize(QSize(self.REFRESH_ICON_SIZE, self.REFRESH_ICON_SIZE))
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.clicked.connect(lambda: self.get_data(city_name=self.config_data["selected_city_name"]))
        # Обране місто
        self.city_lbl = QLabel(text="-")
        self.city_lbl.setObjectName("city")
        # Рядок з іконкою погоди та температурою
        self.weather_img = QLabel()
        self.temp_value = QLabel(text="-°")
        self.temp_value.setObjectName("tempValue")
        # Опис погоди та мін/макс значення температури
        self.desc_lbl = QLabel(text="")
        self.desc_lbl.setObjectName("description")
        self.range_lbl = QLabel(text="—")
        self.range_lbl.setObjectName("tempRange")
        # Розташування
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
        self.selected_city_name = ""
        for ind, city in enumerate(self.config_data["cities"]["ua"]):
            if city == config_data["selected_city_name"]:
                self.selected_city_name = self.config_data["cities"]["eng"][ind]
                break
                
        self.get_data(city_name=self.selected_city_name) # Завантаження погоди

    def get_data(self, city_name: str):
        data = get_weather(city_name, forecast_type = "current", lang=self.config_data["selected_lang"])
        if not data:
            print("Помилка отримання даних з API")   
            self.weather_widget.setObjectName("welcomeWidget")
            self.desc_lbl.setText(get_json("translations.json")[self.config_data["selected_lang"]]["api_data_error"])
            return  
        self.city_lbl.setText(self.config_data["selected_city_name"] if config_data["selected_lang"] == "ua" else city_name)
        self.temp_value.setText(f"{round(data['main']['temp'])}°")
        icon = data['weather'][0]['icon']
        validated_icon = icon if icon != "50n" and icon != "50d" else "04n"
        weather_type = select_weather_type(validated_icon)
        self.weather_widget.setObjectName(weather_type)
        refresh_widget(self.weather_widget)
        self.weather_img.setPixmap(QPixmap(get_image_path(f"{self.config_data['selected_icons_folder']}/{validated_icon}.png")).scaled(
            self.WEATHER_IMAGE_SIZE, self.WEATHER_IMAGE_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
        self.desc_lbl.setText(data["weather"][0]["description"].capitalize())
        self.range_lbl.setText(f"{'Макс.:' if self.config_data['selected_lang'] == 'ua' else 'Max.:'}{round(data['main']['temp_max'])}°, {'мін.:' if self.config_data['selected_lang'] == 'ua' else 'min.:'}{round(data['main']['temp_min'])}°")
    
    def open_main_window(self):
        self.main_window = MainAppWindow(self.MAIN_WINDOW_WIDTH, self.MAIN_WINDOW_HEIGHT, self.config_data, self.weather_widget.objectName())
        self.main_window.show()
        self.close()

main_window = MainWindow(350, 350, config_data)
main_window.show()