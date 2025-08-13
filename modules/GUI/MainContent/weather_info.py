from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from ..city_frame import CityFrame
from ...Tools import get_image_path

class WeatherWidget(QWidget):
    IMAGE_SIZE = 76

    def __init__(self, height, city_frame: CityFrame):
        super().__init__()
        self.setFixedHeight(height)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("cityInfo")
        self.weather_info_layout = QVBoxLayout(self)
        self.weather_info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_info_layout.setSpacing(16)
        self.city_name = QLabel(text=city_frame.city_name.text())
        self.city_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_name.setObjectName("city")
        self.weather_info_layout.addWidget(self.city_name)

        self.temp_img_layout = QHBoxLayout()
        self.temp_img_layout.setSpacing(8)
        self.temp_img = QLabel()
        self.temp_img.setPixmap(QPixmap(get_image_path(f"icons/{city_frame.img_code}.png")).scaled(self.IMAGE_SIZE, self.IMAGE_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.temp_img.setFixedSize(QSize(self.IMAGE_SIZE, self.IMAGE_SIZE))
        self.temp_value = QLabel(text=city_frame.temp_value.text())
        self.temp_value.setObjectName("tempValue")
        self.temp_value.setFixedWidth(self.temp_value.sizeHint().width())
        self.temp_img_layout.addWidget(self.temp_img)
        self.temp_img_layout.addWidget(self.temp_value)
        self.weather_info_layout.addLayout(self.temp_img_layout)

        self.weather_desc = QLabel(city_frame.weather_desc.text().capitalize())
        self.weather_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_desc.setObjectName("description")
        self.weather_info_layout.addWidget(self.weather_desc)
        self.temp_range = QLabel(text=city_frame.temp_max_min.text())
        self.temp_range.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_range.setObjectName("weatherTempRange")
        self.weather_info_layout.addWidget(self.temp_range)