from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from ...Tools import get_image_path

class ForecastBlock(QWidget):
    BLOCK_WIDTH = 55
    BLOCK_HEIGHT = 90
    ICON_SIZE = 25

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
        self.main_layout = QVBoxLayout(self)
        self.time_lbl = QLabel()
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_lbl.setObjectName("forecastText")
        self.main_layout.addWidget(self.time_lbl)
        self.icon_lbl = QLabel()
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.icon_lbl)
        self.temp_lbl = QLabel()
        self.temp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_lbl.setObjectName("forecastText")
        self.main_layout.addWidget(self.temp_lbl)
        self.main_layout.setSpacing(5)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_block(self, time, icon, temp):
        self.time_lbl.setText(time)
        self.icon_lbl.setPixmap(QPixmap(get_image_path(f"icons/{icon}.png")).scaled(
            self.ICON_SIZE, self.ICON_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
        self.temp_lbl.setText(f"{temp}°")