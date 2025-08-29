from PyQt6.QtWidgets import QWidget

def refresh_widget(widget: QWidget):
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)