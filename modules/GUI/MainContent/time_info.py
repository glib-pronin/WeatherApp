from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from ..city_frame import LineFrame
from ...Tools import get_image_path

class TimeWidget(QWidget):
    IMAGE_LABEL_SIZE = 168
    DIAL_SIZE = 150

    def __init__(self, height, city_date_time):
        super().__init__()
        self.setFixedHeight(height)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("cityInfo")
        self.time_info_layout = QVBoxLayout(self)
        self.time_info_layout.setSpacing(20)
        self.time_info_layout.setContentsMargins(20, 10, 20, 10)
        self.time_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.first_line = QVBoxLayout()
        self.first_line.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.first_line.setSpacing(5)
        self.today_label = QLabel(text="Сьогодні")
        self.today_label.setObjectName("todayText")
        self.first_line.addWidget(self.today_label)
        self.line = LineFrame()
        self.first_line.addWidget(self.line, alignment=Qt.AlignmentFlag.AlignTop)
        self.time_info_layout.addLayout(self.first_line)

        self.second_line = QHBoxLayout()
        self.day_of_week = QLabel(text=city_date_time["local_day_of_week"])
        self.day_of_week.setObjectName("dateText")
        self.second_line.addWidget(self.day_of_week)
        self.date = QLabel(text=city_date_time["local_date"])
        self.date.setObjectName("dateText")
        self.second_line.addWidget(self.date, alignment=Qt.AlignmentFlag.AlignRight)
        self.time_info_layout.addLayout(self.second_line)

        self.img_label = QLabel(text="Барса")
        self.img_label.setFixedSize(QSize(self.IMAGE_LABEL_SIZE, self.IMAGE_LABEL_SIZE))
        self.img_label.setPixmap(QPixmap(get_image_path("images/dial.png")).scaled(self.DIAL_SIZE, self.DIAL_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.img_label.setObjectName("dialImg")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_info_layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.time_label = QLabel(text=city_date_time["local_time"], parent=self.img_label)
        self.time_label.setObjectName("timeText")
        self.time_label.setFixedSize(self.img_label.size())
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)