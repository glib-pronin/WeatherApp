from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from ...Tools import get_image_path

class ForecastBlock(QWidget):
    ICON_SIZE = 25

    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.main_layout = QVBoxLayout(self)
        self.time_lbl = QLabel()
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_lbl.setObjectName("forecastText")
        self.main_layout.addWidget(self.time_lbl)
        self.icon_lbl = QLabel()
        self.icon_code = None
        self.icon_lbl.setObjectName("forecastIcon")
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.icon_lbl)
        self.temp_lbl = QLabel()
        self.temp_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.temp_lbl.setObjectName("forecastText")
        self.main_layout.addWidget(self.temp_lbl)
        self.main_layout.setSpacing(10)

    def update_block(self, time, icon, temp, theme):
        self.time_lbl.setText(time)
        self.icon_code = icon
        self.icon_lbl.setPixmap(QPixmap(get_image_path(f"svg_icons/{theme}/{self.icon_code}.svg")).scaled(
            self.ICON_SIZE, self.ICON_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
        self.temp_lbl.setText(f"{temp}°")

    def change_icon_theme(self, theme):
        self.icon_lbl.setPixmap(QPixmap(get_image_path(f"svg_icons/{theme}/{self.icon_code}.svg")).scaled(
            self.ICON_SIZE, self.ICON_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))