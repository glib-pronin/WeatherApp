from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from ..city_frame import LineFrame
from ...Tools import get_weather, make_hourly_data, get_image_path, get_json

class HourlyWidget(QWidget):
    ICON_SIZE = 15
    CHART_WIDTH = 20

    def __init__(self, height, city_eng_name):
        super().__init__()
        self.setFixedHeight(height)
        self.setObjectName("cityInfo")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.theme = get_json("config.json")["selected_theme"]
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        self.main_layout.setSpacing(10)
        # Перший рядок з текстом та лінією
        self.first_line = QVBoxLayout()
        self.first_line.setSpacing(5)
        self.first_line.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.title_label = QLabel(text="Прогноз на сьогодняшній день")
        self.title_label.setObjectName("titleText")
        self.first_line.addWidget(self.title_label)
        self.line = LineFrame()
        self.first_line.addWidget(self.line)
        self.main_layout.addLayout(self.first_line)
        # основна частина з графіком
        self.second_line = QHBoxLayout()
        self.graph_container = QWidget()
        self.graph_container.setFixedHeight(110)
        self.graph_container.setMinimumWidth(600)
        self.graph_container.setObjectName("graphContainer")
        self.second_line.addWidget(self.graph_container)
        self.graph_container_layout = QHBoxLayout(self.graph_container)
        self.graph_container_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_container_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        # Отримання даних та їх формування
        data = get_weather(city_eng_name, forecast_type="daily")
        self.hourly_data = make_hourly_data(data)
        # Рядок з іконками погоди для кожної години
        self.icons_layout = QHBoxLayout()
        self.icons_layout.setSpacing(0)
        self.icons_layout.setContentsMargins(3, 0, 0, 0)
        self.icons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.icons_list = []
        for icon in self.hourly_data["icon_codes"]:
            icon_lbl = QLabel()
            self.icons_list.append(icon_lbl)
            icon_lbl.setFixedWidth(self.ICON_SIZE)
            icon_lbl.setPixmap(QPixmap(get_image_path(f"svg_icons/{self.theme}/{icon}.svg")).scaled(
                self.ICON_SIZE, self.ICON_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            self.icons_layout.addWidget(icon_lbl)
        self.main_layout.addLayout(self.icons_layout)
        # Створення стовпчиків для кожної години
        for chart_height in self.hourly_data["charts_height"]:
            chart = ChartFrame(height=chart_height, width=self.CHART_WIDTH)
            self.graph_container_layout.addWidget(chart, alignment=Qt.AlignmentFlag.AlignBottom)
        # Колонка значень температури
        self.y_axis = QVBoxLayout()
        self.y_axis.setSpacing(5)
        for y in self.hourly_data["y_values"]:
            value = QLabel(f'{y}°')
            value.setFixedWidth(22)
            value.setObjectName("yAxiousValue")
            self.y_axis.addWidget(value)
        self.second_line.addLayout(self.y_axis)
        self.second_line.setSpacing(6)
        self.main_layout.addLayout(self.second_line)

    def resizeEvent(self, a0):
        width = self.graph_container.width()
        chart_spacing = round((width-24*self.CHART_WIDTH)/23)
        icon_spacing = (width-24*self.ICON_SIZE)//23
        self.graph_container_layout.setSpacing(chart_spacing)
        self.icons_layout.setSpacing(icon_spacing)
        super().resizeEvent(a0)

    def update_weather_icons(self, theme):
        self.theme = theme
        for lbl, icon in zip(self.icons_list, self.hourly_data["icon_codes"]):
            lbl.setPixmap(QPixmap(get_image_path(f"svg_icons/{self.theme}/{icon}.svg")).scaled(
                self.ICON_SIZE, self.ICON_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))

class ChartFrame(QFrame):
    def __init__(self, height, width):
        super().__init__()    
        self.setFixedSize(QSize(width, height))
        self.setObjectName("chart")
        