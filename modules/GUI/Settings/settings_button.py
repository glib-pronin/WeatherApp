from PyQt6.QtWidgets import QPushButton, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
from ...Tools import refresh_widget

class SettingsButton(QPushButton):

    def __init__(self, parent: QVBoxLayout, width, height):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.setText("Зберегти")
        self.setObjectName("disableSettingsButton")
        self.setDisabled(True)
        parent.addWidget(self)

    def enable_btn(self):
        if self.objectName() == "disableSettingsButton":
            self.setObjectName("activeSettingsButton")
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setEnabled(True)
            refresh_widget(self)

    def disable_btn(self):
        self.setDisabled(True)
        self.setObjectName("disableSettingsButton")
        refresh_widget(self)


