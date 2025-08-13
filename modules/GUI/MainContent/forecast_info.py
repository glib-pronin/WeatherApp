from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from .forecast_block import ForecastBlock
from ..city_frame import LineFrame
from ..click_filter import ClickFilter
from ...Tools import get_image_path, get_weather, calc_time, get_json

class ForecastWidget(QWidget):
    ARROW_BTN_SIZE = 16

    def __init__(self, height, city_name, city_desc):
        super().__init__()
        self.setFixedHeight(height)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("cityInfo")
        self.click_filter_for_prev = ClickFilter(self.switch_prev)
        self.click_filter_for_next = ClickFilter(self.switch_next)
        self.theme = get_json("config.json")["selected_theme"]
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        self.main_layout.setSpacing(10)

        self.first_line = QVBoxLayout()
        self.first_line.setSpacing(5)
        self.first_line.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.desc_label = QLabel(text=city_desc.capitalize())
        self.desc_label.setObjectName("forecastText")
        self.first_line.addWidget(self.desc_label)
        self.line = LineFrame()
        self.first_line.addWidget(self.line)
        self.main_layout.addLayout(self.first_line)

        self.second_line = QHBoxLayout()
        self.second_line.setSpacing(15)
        self.second_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.forecast_data = {"current_page": 1, "forecasts": []}
        weather_data = get_weather(city_name=city_name, is_forecast=True)
        for forecast in weather_data["list"]:
            data = {
                "time": calc_time(forecast["dt_txt"][11:16], weather_data["city"]["timezone"]),
                "icon": forecast["weather"][0]["icon"] if forecast["weather"][0]["icon"] != "50n" and forecast["weather"][0]["icon"] != "50d" else "04n",
                "temp": round(forecast["main"]["temp"])
            }
            self.forecast_data["forecasts"].append(data)
        self.forecast_blocks = []
        for i in range(10):
            forecast_block = ForecastBlock()
            self.forecast_blocks.append(forecast_block)
            self.second_line.addWidget(forecast_block)
        self.fill_data()
        self.activate_next_btn(self.forecast_data["current_page"])
        self.main_layout.addLayout(self.second_line)

    def activate_prev_btn(self, current_page):
        if current_page > 1:
            self.prev_btn = QLabel()
            self.prev_btn.setPixmap(QPixmap(get_image_path(f"images/prev_{self.theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.prev_btn.installEventFilter(self.click_filter_for_prev)
            self.second_line.insertWidget(0, self.prev_btn)

    def activate_next_btn(self, current_page):
        if current_page < 4:
            self.next_btn = QLabel()
            self.next_btn.setPixmap(QPixmap(get_image_path(f"images/next_{self.theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.next_btn.installEventFilter(self.click_filter_for_next)
            self.second_line.addWidget(self.next_btn)
    
    def update_btn_icons(self, theme):
        self.theme = theme
        if hasattr(self, "next_btn"):
            self.next_btn.setPixmap(QPixmap(get_image_path(f"images/next_{theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
        if hasattr(self, "prev_btn"):
            self.prev_btn.setPixmap(QPixmap(get_image_path(f"images/prev_{self.theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))

    def switch_next(self):
        self.forecast_data["current_page"] = self.forecast_data["current_page"] + 1
        if self.forecast_data["current_page"] == 4:
            self.next_btn.setVisible(False)
        if not hasattr(self, "prev_btn"):
            self.activate_prev_btn(self.forecast_data["current_page"])
        self.prev_btn.setVisible(True)
        self.fill_data()
    
    def switch_prev(self):
        self.forecast_data["current_page"] = self.forecast_data["current_page"] - 1
        if self.forecast_data["current_page"] == 1:
            self.prev_btn.setVisible(False)
        if not hasattr(self, "next_btn"):
            self.activate_next_btn(self.forecast_data["current_page"])
        self.next_btn.setVisible(True)
        self.fill_data()

    def fill_data(self):
        end_ind = self.forecast_data["current_page"]*10
        start_ind = end_ind-10
        for forecast, forecast_block in zip(self.forecast_data["forecasts"][start_ind:end_ind], self.forecast_blocks):
            forecast_block.update_block(forecast["time"], forecast["icon"], forecast["temp"])
