from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt
from .click_filter import ClickFilter

class CityFrame(QWidget):
    def __init__(self, name, code, date_time, temp, desc, tmax, tmin, eng_name, on_click_callback, width=330, height=110):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("cityFrame")
        self.img_code = code
        self.name = name
        self.eng_name = eng_name
        self.date_time = date_time if isinstance(date_time, dict) else {}
        self.click_filter = ClickFilter(lambda city=self: on_click_callback(city_frame=city, change_theme=False))
        self.installEventFilter(self.click_filter)
        # Усі layouts
        self.main_layout = QVBoxLayout(self)
        self.first_row = QHBoxLayout()
        self.last_row = QHBoxLayout()
        self.left_block = QVBoxLayout()
        # Лівий блок: назва та час міста
        self.city_name = QLabel(text=name)
        self.city_name.setObjectName("text2")
        self.city_time = QLabel(text=self.date_time.get("local_time"))
        self.city_time.setObjectName("text3")
        self.left_block.addWidget(self.city_name)
        self.left_block.addWidget(self.city_time)
        # Заповнення першого рядка
        self.temp_value = QLabel(text=f"{round(temp)}°" if temp is not None else "-°")
        self.temp_value.setObjectName("text1")
        self.first_row.addLayout(self.left_block)
        self.first_row.addWidget(self.temp_value, alignment=Qt.AlignmentFlag.AlignRight)
        # Додаткова інформаці
        self.weather_desc = QLabel(text=self.trim_weather_desc(desc))
        self.weather_desc.setObjectName("text3")
        self.temp_max_min = QLabel(text=f"{tmax}°, {tmin}°" if tmax is not None or tmin is not None else "—")
        self.temp_max_min.setObjectName("text3")
        self.last_row.addWidget(self.weather_desc)
        self.last_row.addWidget(self.temp_max_min, alignment=Qt.AlignmentFlag.AlignRight)
        self.line = LineFrame()
        self.main_layout.addLayout(self.first_row)
        self.main_layout.addLayout(self.last_row)
        self.main_layout.addWidget(self.line)
    
    def trim_weather_desc(self, desc: str):
        return f"{desc[:23]}..." if len(desc) > 22 else desc
    
    def trigger_click(self):
        self.click_filter.callback()

    def update_weather(self, code, date_time, temp, desc, tmax, tmin):
        self.img_code = code
        self.date_time = date_time if isinstance(date_time, dict) else {}
        self.city_time.setText(self.date_time.get("local_time"))
        self.temp_value.setText(f"{round(temp)}°" if temp is not None else "-°")
        self.weather_desc.setText(self.trim_weather_desc(desc))
        self.temp_max_min.setText(f"{tmax}°, {tmin}°" if tmax is not None or tmin is not None else "—")

    def change_city_name(self, city_name):
        self.city_name.setText(city_name)

class LineFrame(QFrame):
    def __init__(self):
        super().__init__()    
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain) 
        self.setObjectName("underline")   