from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from .forecast_block import ForecastBlock
from ..city_frame import LineFrame
from ..click_filter import ClickFilter
from ...Tools import get_image_path, get_weather, calc_time, get_json

class ForecastWidget(QWidget):
    ARROW_BTN_SIZE = 16
    BLOCK_WIDTH = 55
    BLOCK_HEIGHT = 100

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
        self.second_line.setSpacing(24)
        self.second_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.forecast_data = {"current_page": 0, "forecasts": []}
        weather_data = get_weather(city_name=city_name, forecast_type="forecast")
        if weather_data:
            for forecast in weather_data["list"]:
                data = {
                    "time": calc_time(forecast["dt_txt"][11:16], weather_data["city"]["timezone"]),
                    "icon": forecast["weather"][0]["icon"] if forecast["weather"][0]["icon"] != "50n" and forecast["weather"][0]["icon"] != "50d" else "04n",
                    "temp": round(forecast["main"]["temp"])
                }
                self.forecast_data["forecasts"].append(data)
        self.forecast_blocks = []
        self.prev_btn = QLabel()
        self.second_line.addWidget(self.prev_btn)
        for i in range(10):
            forecast_block = ForecastBlock(self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
            self.forecast_blocks.append(forecast_block)
            self.second_line.addWidget(forecast_block)
        self.next_btn = QLabel()
        self.second_line.addWidget(self.next_btn)
        self.fill_data()
        self.activate_prev_btn(self.forecast_data["current_page"])
        self.activate_next_btn(self.forecast_data["current_page"])
        self.main_layout.addLayout(self.second_line)

    def resizeEvent(self, a0):
        spacing = (self.width()-self.ARROW_BTN_SIZE*2-len(self.forecast_blocks)*self.BLOCK_WIDTH)//(1+len(self.forecast_blocks))
        self.second_line.setSpacing(spacing)
        return super().resizeEvent(a0)

    def activate_prev_btn(self, current_page):
        if current_page > 0:
            self.prev_btn.setPixmap(QPixmap(get_image_path(f"images/prev_{self.theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.prev_btn.installEventFilter(self.click_filter_for_prev)
        else:
            self.prev_btn.setCursor(Qt.CursorShape.ArrowCursor)
            self.prev_btn.setPixmap(QPixmap(get_image_path(f"images/prev_{self.theme}_disable.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))

    def activate_next_btn(self, current_page):
        if current_page < len(self.forecast_data["forecasts"]) - 10:
            self.next_btn.setPixmap(QPixmap(get_image_path(f"images/next_{self.theme}.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
            self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.next_btn.installEventFilter(self.click_filter_for_next)
        else:
            self.next_btn.setCursor(Qt.CursorShape.ArrowCursor)
            self.next_btn.setPixmap(QPixmap(get_image_path(f"images/next_{self.theme}_disable.png")).scaled(
                self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
    
    def switch_next(self):
        if self.forecast_data["current_page"] < len(self.forecast_data["forecasts"]) - 10:
            self.forecast_data["current_page"] = self.forecast_data["current_page"] + 1
            self.refresh_ui()
    
    def switch_prev(self):
        if self.forecast_data["current_page"] > 0:
            self.forecast_data["current_page"] = self.forecast_data["current_page"] - 1
            self.refresh_ui()
   
    def refresh_ui(self):
        self.activate_prev_btn(self.forecast_data["current_page"])
        self.activate_next_btn(self.forecast_data["current_page"])
        self.fill_data()

    def update_btn_icons(self, theme):
        self.theme = theme
        self.next_btn.setPixmap(QPixmap(get_image_path(f"images/next_{theme}{'' if self.forecast_data['current_page'] < len(self.forecast_data['forecasts']) - 10 else '_disable'}.png")).scaled(
            self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
        self.prev_btn.setPixmap(QPixmap(get_image_path(f"images/prev_{self.theme}{'' if self.forecast_data['current_page'] > 0 else '_disable'}.png")).scaled(
            self.ARROW_BTN_SIZE, self.ARROW_BTN_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
        for forecast_block in self.forecast_blocks:
            forecast_block.change_icon_theme(theme)

    def fill_data(self):
        start_ind = self.forecast_data["current_page"]
        end_ind = start_ind+10
        print(start_ind, end_ind)
        for forecast, forecast_block in zip(self.forecast_data["forecasts"][start_ind:end_ind], self.forecast_blocks):
            forecast_block.update_block(forecast["time"], forecast["icon"], forecast["temp"], theme=self.theme)
