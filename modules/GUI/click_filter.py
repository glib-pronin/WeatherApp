from PyQt6.QtCore import QObject, QEvent

class ClickFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def eventFilter(self, a0, a1):
        if a1.type() == QEvent.Type.MouseButtonPress:
            self.callback()
            return True
        return super().eventFilter(a0, a1)