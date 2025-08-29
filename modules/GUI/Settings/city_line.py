from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from ..click_filter import ClickFilter
from ...Tools import get_image_path

class CityLine(QWidget):
    LINE_WIDTH = 512
    LINE_HEIGHT = 32
    ICON_SIZE = 16

    def __init__(self, parent: QHBoxLayout, text, index, signal, on_delete_callback):
        super().__init__()
        self.parent = parent
        self.parent.addWidget(self)
        self.setFixedSize(QSize(self.LINE_WIDTH, self.LINE_HEIGHT))
        self.index = index
        self.click_filter = ClickFilter(lambda: on_delete_callback(self.index))
        self.signal = signal
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.city = QLabel(text=text)
        self.city.setObjectName("cityLine")
        self.main_layout.addWidget(self.city)
        # Кнопка видалення
        self.delete_btn = QLabel()
        self.delete_btn.setPixmap(QPixmap(get_image_path("images/delete_icon.png")).scaled(
            self.ICON_SIZE, self.ICON_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.delete_btn)
        self.delete_btn.installEventFilter(self.click_filter)

    def delete_city_line(self, city_line_list):
        self.signal.emit({"delete_city": self.index})
        city_line_list.pop(self.index)
        for ind, city_line in enumerate(city_line_list): # Змінюємо індекси
            city_line.index = ind
        self.parent.removeWidget(self) # Видаляємо місто
        self.deleteLater()
