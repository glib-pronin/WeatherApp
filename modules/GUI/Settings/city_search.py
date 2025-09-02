from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QLineEdit, QScrollArea, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from .settings_button import SettingsButton
from .city_line import CityLine
from ...Tools import get_json, get_weather, get_coords_by_city, MapLoader, prepare_coords, get_city_name_by_coords, get_translated_city_name

class CitySearchWidget(QWidget):
    COMBO_WIDTH = 239
    COMBO_HEIGHT = 32
    INPUT_WIDTH = 150
    SCROLL_AREA_WIDTH = 544
    SCROLL_AREA_HEIGHT = 160
    TITLE_HEIGHT = 21
    MAP_WIDTH = 289
    MAP_HEIGHT = 256

    dataChangedSignal = pyqtSignal(object)

    def __init__(self, height, lang, lang_dict):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("settingsMainContent")
        self.setFixedHeight(height)
        self.mode = None
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
        self.inner_layout = QVBoxLayout()
        self.inner_layout.setSpacing(24)
        self.inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.combo_boxes_layout = QVBoxLayout()
        self.combo_boxes_layout.setSpacing(16)
        self.inner_layout.addLayout(self.combo_boxes_layout)
        self.adding_city_layout.addLayout(self.inner_layout)
        # Контейнер для карти
        self.map_container = QLabel()
        self.map_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_container.setFixedSize(QSize(self.MAP_WIDTH, self.MAP_HEIGHT))
        self.adding_city_layout.addWidget(self.map_container)
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
        self.input_button_layout = QHBoxLayout()
        self.input_button_layout.setSpacing(10)
        self.coord_input = QLineEdit()
        self.coord_input.textEdited.connect(self.handle_coord_enter)
        self.coord_input.setFixedSize(QSize(self.INPUT_WIDTH, self.COMBO_HEIGHT))
        self.coord_input.setPlaceholderText(self.lang_dict[self.lang]["coords_placeholder"])
        self.input_button_layout.addWidget(self.coord_input)
        self.map_button = SettingsButton(self.input_button_layout, 69, 38)
        self.map_button.setText(self.lang_dict[self.lang]["map_button_text"])
        self.map_button.clicked.connect(self.show_map_from_input)
        self.coord_layout.addLayout(self.input_button_layout)
        # Кнопка збереження та лейбл для повідомлень
        self.btns_layout = QHBoxLayout()
        self.btns_layout.setSpacing(8)
        self.btns_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.save_btn = SettingsButton(self.btns_layout, 105, 38)
        self.save_btn.clicked.connect(self.save_handler)
        self.save_btn.setText(self.lang_dict[self.lang]["save_btn_caption"])
        self.message_lbl = QLabel()
        self.message_lbl.setFixedHeight(self.TITLE_HEIGHT)
        self.message_lbl.setObjectName("messageLabel")
        self.message_lbl.setVisible(False)
        self.btns_layout.addWidget(self.message_lbl)
        self.inner_layout.addLayout(self.btns_layout)
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
        self.city_combo.currentIndexChanged.connect(self.handle_city_combo_change) # При виборі міста активується кнопка

    def handle_coord_enter(self):
        if self.mode == "combo":
            self.city_combo.clear()
            self.set_combo_placeholder(self.country_combo, self.lang_dict[self.lang]["country_combo_placeholder"])
            self.cleanup_loader()
            self.map_container.clear()
        self.mode = "input"
        self.save_btn.disable_btn()
        self.map_button.enable_btn()

    def show_map_from_input(self):
        coords = prepare_coords(self.coord_input.text())
        print(coords)
        if coords is None:
            self.map_container.setText(self.lang_dict[self.lang]["wrong_coord_msg"])
        else:
            self.map_container.setText(self.lang_dict[self.lang]["map_loading"])
            self.set_loader(coords)
        self.map_button.disable_btn()

    def handle_city_combo_change(self):
        if self.city_combo.currentIndex() > -1:
            print("city_combo")
            self.save_btn.disable_btn()
            self.map_container.clear()
            country = self.get_country_by_code(self.country_combo.currentData()) 
            city = country["cities"]["eng"][self.city_combo.currentIndex()] 
            print(city)
            coords = get_coords_by_city(city_name=city, country_name=country["name"]["eng"])
            if coords:
                print(coords)
                self.map_container.setText(self.lang_dict[self.lang]["map_loading"])
                self.cleanup_loader()
                self.set_loader(coords)
            else:
                self.save_btn.enable_btn()

    def set_pixmap(self, pix):
        if hasattr(self, "map_container"):
            if pix is not None:
                self.map_container.setPixmap(pix)
                self.save_btn.enable_btn()
            else:
                self.map_container.setText(self.lang_dict[self.lang]["wrong_coord_msg"])

    def save_handler(self):
        city_names = self.get_city_names()
        if city_names:
            print("here we go")
            if city_names[0] in self.cities_list["eng"]: # ЯКщо таке місто вже наявне, пририваємо операцію
                self.message_lbl.setVisible(True)
                self.message_lbl.setText(self.lang_dict[self.lang]["existed_city_error"])
            else:
                data = get_weather(city_names[0], forecast_type="current", lang=self.lang) # Отримуємо дані
                if data: # Якщо прийшли 
                    self.cities_list["eng"].append(city_names[0])
                    self.cities_list["ua"].append(city_names[1])
                    self.add_city(city_names[0] if self.lang == "eng" else city_names[1]) # Додаємо місто в список на екрані
                    data["city_ua"] = city_names[1]
                    data["name"] = city_names[0]
                    self.dataChangedSignal.emit({"added_city": data})
                    self.message_lbl.setVisible(False)
                else: 
                    self.message_lbl.setVisible(True)
                    self.message_lbl.setText(self.lang_dict[self.lang]["not_found_city_error"])
        self.set_combo_placeholder(self.country_combo, self.lang_dict[self.lang]["country_combo_placeholder"])
        self.city_combo.clear() # Очищаємо комбо з містами
        self.coord_input.clear() 
        self.save_btn.disable_btn()
        self.map_container.clear()

    def get_city_names(self):
        if self.mode == "combo" and self.city_combo.currentIndex() > -1:
            country = self.get_country_by_code(self.country_combo.currentData()) # Обрана країна
            current_index = self.city_combo.currentIndex() # Поточний індекс обраного міста в списку
            city = country["cities"]["eng"][current_index] # Нзава англійською
            city_ua = country["cities"]["ua"][current_index] # Українською
        elif self.mode == "input":
            coords = prepare_coords(self.coord_input.text())
            city = get_city_name_by_coords(coords[0], coords[1])
            if not city:
                self.message_lbl.setVisible(True)
                self.message_lbl.setText(self.lang_dict[self.lang]["not_found_city_error"])
                self.map_container.clear()
                return
            translated_data = get_translated_city_name(city)
            city_ua = translated_data[0] if len(translated_data) > 0 else city
        else: 
            return
        return (city, city_ua)

    def add_city(self, city_name):
        city_line = CityLine(self.scroll_content_Layout, city_name, len(self.city_line_list), self.dataChangedSignal, self.delete_city)
        self.city_line_list.append(city_line)

    def set_combo_placeholder(self, combo, placeholder):
        combo.setCurrentIndex(-1)
        combo.setEditable(True)
        combo.lineEdit().setPlaceholderText(placeholder)
    
    def load_countries(self):
        for country in self.countries:
            self.country_combo.addItem(country["name"][self.lang], country["code"])
    
    def load_cities(self, current_code):
        self.mode = "combo"
        self.city_combo.blockSignals(True)
        self.city_combo.clear()
        if current_code:
            country = self.get_country_by_code(current_code)
            self.city_combo.addItems(country["cities"][self.lang])
            self.city_combo.setCurrentIndex(-1)
            self.save_btn.disable_btn()
            self.map_button.disable_btn()
            self.coord_input.clear()
            self.map_container.clear()
            self.cleanup_loader()
        self.city_combo.blockSignals(False)
            
    def get_country_by_code(self, code):
        for country in self.countries:
                if country["code"] == code:
                    return country

    def delete_city(self, index):
        self.city_line_list[index].delete_city_line(self.city_line_list)
        self.cities_list = get_json("config.json")["cities"]
        print(self.cities_list)

    def set_loader(self, coords):
        self.loader = MapLoader(str(coords[0]).strip(), str(coords[1]).strip())
        self.loader.finished.connect(lambda pix: self.set_pixmap(pix["pixmap"]))
        self.loader.start()

    def cleanup_loader(self):
        if hasattr(self, "loader") and self.loader.isRunning():
            try:
                self.loader.finished.disconnect()
            except TypeError:
                pass