from PyQt6.QtWidgets import QPushButton, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
from ...Tools import refresh_widget

class SaveButton(QPushButton):
    BUTTON_WIDTH = 105
    BUTTON_HEIGHT = 38

    def __init__(self, parent: QVBoxLayout):
        super().__init__()
        self.setFixedSize(QSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        self.setText("Зберегти")
        self.setObjectName("disableSaveButton")
        self.setDisabled(True)
        parent.addWidget(self)

    def enable_btn(self):
        if self.objectName() == "disableSaveButton":
            self.setObjectName("activeSaveButton")
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setEnabled(True)
            refresh_widget(self)

    def disable_btn(self):
        self.setDisabled(True)
        self.setObjectName("disableSaveButton")
        refresh_widget(self)


