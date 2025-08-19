from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

class WindowsTopBar(QWidget):
    def __init__(self, parent, height):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(height)