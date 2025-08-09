from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from ..Tools import get_image_path
from .click_filter import ClickFilter

class MainContent(QWidget):

    SEARCHING_PANEL_HEIGHT = 36
    BASE_ADDING_WIDTH = 100
    ERROR_PADDING = 15
    INPUT_WIDTH = 255
    ICON_SIZE = 12

    def __init__(self, width, height, config_data, on_click_callback):
        print(width, height)
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.setObjectName("mainContent")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.click_filter = ClickFilter(on_click_callback)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.top_panel = QHBoxLayout()

        self.adding_frame = QWidget()
        self.adding_frame.setFixedSize(QSize(self.BASE_ADDING_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.adding_frame.setObjectName("cityAddFrame")
        self.adding_layout = QHBoxLayout(self.adding_frame)
        self.plus_icon = QLabel(text="+")
        self.plus_icon.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.plus_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plus_icon.setObjectName("plusIcon")
        self.frame_text = QLabel(text="Додати")
        self.frame_text.setObjectName("cityAddFrameText")
        self.adding_layout.addWidget(self.plus_icon)
        self.adding_layout.addWidget(self.frame_text)
        self.adding_frame.setVisible(False)
        self.adding_frame.installEventFilter(self.click_filter)

        self.search_layout = QHBoxLayout()
        self.search_icon = QLabel()
        self.set_search_icon(config_data["selected_theme"])
        self.search_icon.setFixedSize(QSize(self.SEARCHING_PANEL_HEIGHT, self.SEARCHING_PANEL_HEIGHT))
        self.search_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_icon.setObjectName("searchIcon")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setFixedSize(QSize(self.INPUT_WIDTH, self.SEARCHING_PANEL_HEIGHT))
        self.search_input.textEdited.connect(self.show_adding_frame)

        self.search_layout.addWidget(self.search_icon)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.setSpacing(0)
        self.top_panel.addWidget(self.adding_frame)
        self.top_panel.addLayout(self.search_layout)
        self.top_panel.setSpacing(10)
        self.top_panel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addLayout(self.top_panel)

    def set_search_icon(self, theme: str):
        self.search_icon.setPixmap(QPixmap(get_image_path(f"images/search_icon_{theme}.png")).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    
    def show_adding_frame(self):
        self.adding_frame.setVisible(bool(self.search_input.text().strip()))
        self.normalize_adding_frame()

    def handle_search_result(self, success: bool, error: str = None):
        self.search_input.clear()
        if success:
            self.adding_frame.setVisible(False)
            return
        self.normalize_adding_frame(text=error, plus_visible=False)

    def normalize_adding_frame(self, text: str = "Додати", plus_visible: bool = True):
        self.frame_text.setText(text)
        self.plus_icon.setVisible(plus_visible)
        frame_width = self.frame_text.sizeHint().width()+self.ERROR_PADDING if not plus_visible else self.BASE_ADDING_WIDTH
        self.adding_frame.setFixedWidth(frame_width)



