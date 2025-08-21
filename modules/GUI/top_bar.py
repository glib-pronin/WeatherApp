from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import Qt, QSize
import platform

class WindowsTopBar(QWidget):
    ICON_SIZE = 16

    def __init__(self, main_window, height, app_name):
        super().__init__()
        self.os_name = platform.system() # Отримуємо назву ОС
        self.old_pos = None
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(height)
        self.setObjectName("topBar")
        self.main_window = main_window
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 0, 0, 0)
        # Назва
        self.title = QLabel(app_name)
        self.title.setObjectName("topPanelTitle")
        # Якщо ОС - Windows
        if self.os_name == "Windows":
            self.main_layout.addWidget(self.title)
            self.btn_min = QPushButton(text="—")
            self.btn_max = QPushButton("▢")
            self.btn_close = QPushButton(text="✕")
            for btn in (self.btn_min, self.btn_max, self.btn_close):
                btn.setFixedSize(QSize(40, 30))
                self.main_layout.addWidget(btn)
            self.btn_max.setObjectName("commandBtnMaxBig")
            self.btn_min.setObjectName("commandBtnMin")
            self.btn_close.setObjectName("commandBtnClose")
        else: 
            self.main_layout.setContentsMargins(10, 0, 10, 0)
            self.btn_min = QPushButton()
            self.btn_max = QPushButton()
            self.btn_close = QPushButton()
            for btn in (self.btn_close, self.btn_max, self.btn_min):
                btn.setFixedSize(QSize(14, 14))
                self.main_layout.addWidget(btn)
            self.btn_close.setObjectName("redBtn")
            self.btn_min.setObjectName("yellowBtn")
            self.btn_max.setObjectName("greenBtn")
            self.main_layout.addStretch()
            self.main_layout.addWidget(self.title)
        # Вішаємо обробники на кнопки
        self.btn_min.clicked.connect(self.main_window.showMinimized)
        self.btn_max.clicked.connect(self.toggle_btn_max)
        self.btn_close.clicked.connect(self.main_window.close)

    def toggle_btn_max(self):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
            if self.os_name != "Darwin":
                self.btn_max.setText("▢")
                self.btn_max.setObjectName("commandBtnMaxBig")
        else:
            self.main_window.showMaximized()
            if self.os_name != "Darwin":
                self.btn_max.setText("❐")
                self.btn_max.setObjectName("commandBtnMaxSmall")
        self.refresh_style(self.main_window.central_widget)
        self.refresh_style(self.main_window.side_bar)
        self.refresh_style(self.btn_max)
        self.refresh_style(self.btn_close)
        self.refresh_style(self)

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.old_pos = a0.globalPosition().toPoint() # Отримуємо глобальну позицію курсору під час кліку ЛКМ
        return super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0):
        if self.old_pos and not self.main_window.isMaximized(): # Якщо ЛКМ натиснута та вікно не розгорнуте
            delta = a0.globalPosition().toPoint() - self.old_pos # Рахуємо вектор
            self.main_window.move(self.main_window.pos() + delta)
            self.old_pos = a0.globalPosition().toPoint()
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0):
        self.old_pos = None # Очищаємо позицію
        return super().mouseReleaseEvent(a0)
    
    def mouseDoubleClickEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.toggle_btn_max()
        return super().mouseDoubleClickEvent(a0)
    
    def refresh_style(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)