from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QLineEdit, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from .save_button import SaveButton
from .city_line import CityLine
from ...Tools import get_json, get_weather

class CitySearchWidget(QWidget):
    COMBO_WIDTH = 239
    COMBO_HEIGHT = 32
    SCROLL_AREA_WIDTH = 544
    SCROLL_AREA_HEIGHT = 160
    TITLE_HEIGHT = 21

    dataChangedSignal = pyqtSignal(object)

    def __init__(self, height, lang, lang_dict):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("settingsMainContent")
        self.setFixedHeight(height)
        self.lang = lang
        self.lang_dict = lang_dict
        self.countries = get_json("countries_cities.json")
        self.cities_list = get_json("config.json")["cities"]
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(24)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(24, 0, 0, 0)
        # Надпис
        self.title = QLabel(text=self.lang_dict[self.lang]["searching_city_section"])
        self.title.setFixedHeight(self.TITLE_HEIGHT)
        self.title.setObjectName("settingsSectionContentTitle")
        self.main_layout.addWidget(self.title)
        # Основні layouts
        self.adding_city_layout = QHBoxLayout()
        self.adding_city_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.adding_city_layout.setSpacing(16)
        self.main_layout.addLayout(self.adding_city_layout)
        self.combo_boxes_layout = QVBoxLayout()
        self.combo_boxes_layout.setSpacing(16)
        self.adding_city_layout.addLayout(self.combo_boxes_layout)
        # Комбо для країн
        self.country_layout = QVBoxLayout()
        self.combo_boxes_layout.addLayout(self.country_layout)
        self.country_layout.setSpacing(8)
        self.country_caption = QLabel(text=self.lang_dict[self.lang]["country_combo_caption"])
        self.country_caption.setObjectName("settingsSectionContentCaption")
        self.country_layout.addWidget(self.country_caption)
        self.country_combo = QComboBox()
        self.load_countries() # Одразу заповнюємо
        # При виборі країни заповнюємо комбо міст
        self.country_combo.currentIndexChanged.connect(lambda: self.load_cities(self.country_combo.currentData()))
        self.country_combo.setFixedSize(QSize(self.COMBO_WIDTH, self.COMBO_HEIGHT))
        self.country_layout.addWidget(self.country_combo)
        # Комбо для міст
        self.city_layout = QVBoxLayout()
        self.combo_boxes_layout.addLayout(self.city_layout)
        self.city_layout.setSpacing(8)
        self.city_caption = QLabel(text=self.lang_dict[self.lang]["city_combo_caption"])
        self.city_caption.setObjectName("settingsSectionContentCaption")
        self.city_layout.addWidget(self.city_caption)
        self.city_combo = QComboBox()
        self.city_combo.setFixedSize(QSize(self.COMBO_WIDTH, self.COMBO_HEIGHT))
        self.city_layout.addWidget(self.city_combo)
        # Поле для координат
        self.coord_layout = QVBoxLayout()
        self.combo_boxes_layout.addLayout(self.coord_layout)
        self.coord_layout.setSpacing(8)
        self.coord_caption = QLabel(text=self.lang_dict[self.lang]["coords_combo_caption"])
        self.coord_caption.setObjectName("settingsSectionContentCaption")
        self.coord_layout.addWidget(self.coord_caption)
        self.coord_input = QLineEdit()
        self.coord_input.setFixedSize(QSize(self.COMBO_WIDTH, self.COMBO_HEIGHT))
        self.coord_input.setPlaceholderText("(WGS 84,UTM,MGRS)")
        self.coord_layout.addWidget(self.coord_input)
        # Кнопка збереження та лейбл для повідомлень
        self.btns_layout = QHBoxLayout()
        self.btns_layout.setSpacing(8)
        self.btns_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.save_btn = SaveButton(self.btns_layout)
        self.save_btn.clicked.connect(self.save_handler)
        self.save_btn.setText(self.lang_dict[self.lang]["save_btn_caption"])
        self.message_lbl = QLabel()
        self.message_lbl.setFixedHeight(self.TITLE_HEIGHT)
        self.message_lbl.setObjectName("messageLabel")
        self.message_lbl.setVisible(False)
        self.btns_layout.addWidget(self.message_lbl)
        self.main_layout.addLayout(self.btns_layout)
        # Список доданих міст
        self.added_cities_layout = QVBoxLayout()
        self.added_cities_layout.setSpacing(16)
        self.main_layout.addLayout(self.added_cities_layout)
        self.added_cities_title = QLabel(text=self.lang_dict[self.lang]["added_cities_title"])
        self.added_cities_title.setFixedHeight(self.TITLE_HEIGHT)
        self.added_cities_title.setObjectName("settingsSectionContentTitle")
        self.added_cities_layout.addWidget(self.added_cities_title)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setFixedSize(QSize(self.SCROLL_AREA_WIDTH, self.SCROLL_AREA_HEIGHT))
        self.added_cities_layout.addWidget(self.scroll_area)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("settingsScrollContent")
        self.scroll_content_Layout = QVBoxLayout(self.scroll_content)
        self.scroll_content_Layout.setSpacing(0)
        self.scroll_content_Layout.setContentsMargins(16, 16, 16, 16)
        self.scroll_content_Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.city_line_list = []
        for ind, city in enumerate(self.cities_list[self.lang]):
            city_line = CityLine(self.scroll_content_Layout, city, ind, self.dataChangedSignal, self.delete_city)
            self.city_line_list.append(city_line)
        self.scroll_area.setWidget(self.scroll_content)
        
        self.set_combo_placeholder(self.country_combo, self.lang_dict[self.lang]["country_combo_placeholder"])
        self.set_combo_placeholder(self.city_combo, self.lang_dict[self.lang]["city_combo_placeholder"])
        self.city_combo.currentIndexChanged.connect(self.save_btn.enable_btn) # При виборі міста активується кнопка

    def save_handler(self):
        country = self.get_country_by_code(self.country_combo.currentData()) # Обрана країна
        current_index = self.city_combo.currentIndex() # Поточний індекс обраного міста в списку
        city = country["cities"]["eng"][current_index] # Нзава англійською
        city_ua = country["cities"]["ua"][current_index] # Українською
        if city in self.cities_list["eng"]: # ЯКщо таке місто вже наявне, пририваємо операцію
            self.message_lbl.setVisible(True)
            self.message_lbl.setText(self.lang_dict[self.lang]["existed_city_error"])
        else:
            data = get_weather(city, forecast_type="current", lang=self.lang) # Отримуємо дані
            if data: # Якщо прийшли 
                self.cities_list["eng"].append(city)
                self.cities_list["ua"].append(city_ua)
                self.add_city(city if self.lang == "eng" else city_ua) # Додаємо місто в список на екрані
                data["city_ua"] = city_ua
                data["name"] = city
                code = data['weather'][0]['icon']
                data['weather'][0]['icon'] = code if code != "50n" and code != "50d" else "04n"
                self.dataChangedSignal.emit({"added_city": data})
                self.message_lbl.setVisible(False)
            else: 
                self.message_lbl.setVisible(True)
                self.message_lbl.setText(self.lang_dict[self.lang]["not_found_city_error"])
        self.set_combo_placeholder(self.country_combo, self.lang_dict[self.lang]["country_combo_placeholder"])
        self.city_combo.clear() # Очищаємо комбо з містами
        self.save_btn.disable_btn()

    def add_city(self, city_name):
        city_line = CityLine(self.scroll_content_Layout, city_name, len(self.city_line_list), self.dataChangedSignal, self.delete_city)
        self.city_line_list.append(city_line)

    def set_combo_placeholder(self, combo, placeholder):
        combo.setCurrentIndex(-1)
        combo.setEditable(True)
        # combo.lineEdit().setReadOnly(True)
        combo.lineEdit().setPlaceholderText(placeholder)
    
    def load_countries(self):
        for country in self.countries:
            self.country_combo.addItem(country["name"][self.lang], country["code"])
    
    def load_cities(self, current_code):
        self.city_combo.clear()
        if current_code:
            country = self.get_country_by_code(current_code)
            self.city_combo.addItems(country["cities"][self.lang])

    def get_country_by_code(self, code):
        for country in self.countries:
                if country["code"] == code:
                    return country

    def delete_city(self, index):
        self.city_line_list[index].delete_city_line(self.city_line_list)
        self.cities_list = get_json("config.json")["cities"]
        print(self.cities_list)